import pandas as pd

from transformers import pipeline
from typing import Optional, List

from transformers import pipeline

def analyze_sentiment(df, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
    # Initialize the pipeline
    sentiment_pipe = pipeline("sentiment-analysis", model=model_name)

    # Truncate texts safely
    df["clean_text"] = df["clean_text"].astype(str).apply(lambda x: x[:2000])

    # Analyze in batches to avoid OOM errors
    results = sentiment_pipe(df["clean_text"].tolist(), truncation=True)

    df["sentiment_label"] = [r["label"] for r in results]
    df["sentiment_score"] = [r["score"] for r in results]
    return df
