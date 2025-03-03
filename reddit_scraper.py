import datetime
import os
import praw
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Initialize Reddit API client
def connect_to_reddit():
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT')
    )
    return reddit

def scrape_livestreamfail(limit=100):
    reddit = connect_to_reddit()
    subreddit = reddit.subreddit('livestreamfail')
    posts = []

    for post in subreddit.hot(limit=limit):
        posts.append({
            'title': post.title,
            'score': post.score,
            'id': post.id,
            'url': post.url,
            'num_comments': post.num_comments,
            # 'created': datetime.fromtimestamp(post.created_utc),
            'body': post.selftext
        })

    df = pd.DataFrame(posts)
    return df

if __name__ == "__main__":
    df = scrape_livestreamfail()
    df.to_csv('livestreamfail_data.csv', index=False)
    print(f"Scraped {len(df)} posts from r/livestreamfail")
