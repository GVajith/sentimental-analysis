import pandas as pd
import snscrape.modules.twitter as sntwitter
import os
Twitter_token=os.getenv("TWITTER_BEARER_TOKEN")
def fetch_twitter_tweets(query: str, limit: int = 100):
    bearer = Twitter_token
    tweets = []

    if bearer:
        import tweepy
        client = tweepy.Client(bearer_token=bearer)
        response = client.search_recent_tweets(query=query, max_results=min(limit, 100))
        for tweet in response.data or []:
            tweets.append({
                "id": f"twitter_{tweet.id}",
                "source": "twitter",
                "raw_text": tweet.text
            })
        return pd.DataFrame(tweets)

    raise Exception("No Twitter Bearer Token configured — snscrape currently broken.")
