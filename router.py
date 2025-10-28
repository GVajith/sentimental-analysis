from fastapi import APIRouter, HTTPException, Query

from dotenv import load_dotenv
import os
from typing import Optional, List
from reddit import fetch_reddit_posts
from twitter import fetch_twitter_tweets
from datacombining import combine_and_clean
from sentiment_analysis import analyze_sentiment
from df_stream import dataframe_to_stream

load_dotenv()
router = APIRouter()
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")
TWITTER_BEARER = os.getenv("TWITTER_BEARER_TOKEN")

@router.post("/pipeline")
def full_pipeline(
    subreddit: Optional[str] = Query(None, description="subreddit name to fetch (e.g. technology)"),
    reddit_limit: int = Query(100, ge=1, le=1000, description="max posts from reddit"),
    twitter_query: Optional[str] = Query(None, description="twitter search query (e.g. 'ai lang:en')"),
    twitter_limit: int = Query(100, ge=1, le=1000, description="max tweets to fetch"),
    model_name: Optional[str] = "distilbert-base-uncased-finetuned-sst-2-english",
    source_preference: Optional[str] = Query("both", description="which sources to fetch: 'reddit', 'twitter', or 'both'")
):

    try:
        dfs = []
        want_reddit = source_preference in ("both", "reddit") and subreddit is not None
        want_twitter = source_preference in ("both", "twitter") and twitter_query is not None

        if not (want_reddit or want_twitter):
            raise HTTPException(status_code=400, detail="Provide at least one of subreddit or twitter_query (and ensure source_preference permits it).")

        if want_reddit:
            try:
                df_r = fetch_reddit_posts(subreddit, limit=reddit_limit)
                dfs.append(df_r)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error fetching reddit: {str(e)}")

        if want_twitter:
            try:
                df_t = fetch_twitter_tweets(twitter_query, limit=twitter_limit)
                dfs.append(df_t)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error fetching twitter: {str(e)}")

        combined = combine_and_clean(dfs)
        if combined.empty:
            raise HTTPException(status_code=204, detail="No usable text after cleaning.")

        # 4) sentiment analysis
        try:
            analyzed = analyze_sentiment(combined, model_name=model_name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")

        # 5) return CSV stream
        return dataframe_to_stream(analyzed, filename="combined_analyzed.csv")

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(exc)}")