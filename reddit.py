# social_pipeline_router.py
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse
from dotenv import load_dotenv
import os
import praw
import pandas as pd
import snscrape.modules.twitter as sntwitter
import io
from transformers import pipeline
from typing import Optional, List

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")


def check_reddit_credentials():
    if not CLIENT_ID or not CLIENT_SECRET or not USER_AGENT:
        raise RuntimeError("Missing Reddit credentials. Fill CLIENT_ID, CLIENT_SECRET, USER_AGENT in .env")

def fetch_reddit_posts(subreddit: str, limit: int = 100) -> pd.DataFrame:
    check_reddit_credentials()
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         user_agent=USER_AGENT)
    posts = []
    sub = reddit.subreddit(subreddit)
    for post in sub.hot(limit=limit):
        title = post.title or ""
        selftext = post.selftext or ""
        text = f"{title}\n\n{selftext}".strip()
        posts.append({
            "id": f"reddit_{post.id}",
            "source": "reddit",
            "created_at": getattr(post, "created_utc", None),
            "raw_text": text,
            "score": getattr(post, "score", None),
            "url": getattr(post, "url", None)
        })
    return pd.DataFrame(posts)
