import os
import pandas as pd
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

# Load environment variables from .env file
load_dotenv()

class RAGChatbot:
    def __init__(self):
        self.df = pd.read_csv('livestreamfail_data.csv')
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.vectorstore = self._create_vectorstore()
        self.memory = ConversationBufferMemory(input_key="input", memory_key="chat_history")
        
        # Initialize OpenAI with the API key from environment variables
        self.llm = OpenAI(temperature=0.7, openai_api_key=os.getenv('OPENAI_API_KEY'))
        self.chain = self._create_chain()

    def _clean_data(self):
        self.df['title'] = self.df['title'].astype(str)
        self.df['body'] = self.df['body'].astype(str)
        
        self.df['title'] = self.df['title'].replace('nan', '')
        self.df['body'] = self.df['body'].replace('nan', '')

    def _create_vectorstore(self):
        combined_text = (self.df['title'] + ' ' + self.df['body']).tolist()
        
        combined_text = [text for text in combined_text if text is not None]
        
        embeddings = self.model.encode(combined_text)
        
        return FAISS.from_embeddings(embeddings.tolist(), combined_text)

    def _create_chain(self):
        template = """
        You are a helpful chatbot specialized in r/livestreamfail subreddit content.
        Chat History: {chat_history}

        Relevant information from r/livestreamfail:
        {context}

        User Question: {input}

        Please provide a helpful, accurate response based on the information above:
        """
        prompt = PromptTemplate(input_variables=["input", "chat_history", "context"], template=template)
        return LLMChain(llm=self.llm, prompt=prompt, memory=self.memory)

    def get_response(self, query):
        relevant_docs = self.vectorstore.similarity_search(query, k=3)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        response = self.chain.predict(input=query, context=context)
        return response

# Create an instance of RAGChatbot
chatbot = RAGChatbot()
