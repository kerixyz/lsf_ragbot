import streamlit as st
from ragbot import RAGChatbot

st.set_page_config(page_title="r/LivestreamFail Chatbot", page_icon="🤖")

st.title("r/LivestreamFail Chatbot")

chatbot = RAGChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know about r/LivestreamFail?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = chatbot.get_response(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

st.sidebar.title("About")
st.sidebar.info(
    "This chatbot uses RAG (Retrieval Augmented Generation) to answer questions about r/LivestreamFail. "
    "It's powered by the latest data scraped from the subreddit."
)
