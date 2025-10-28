import pandas as pd
from typing import Optional, List
from datacleaning import clean_text

def combine_and_clean(dfs: List[pd.DataFrame]) -> pd.DataFrame:
    combined = pd.concat(dfs, ignore_index=True, sort=False)
    combined["raw_text"] = combined.get("raw_text", pd.Series([""] * len(combined))).fillna("").astype(str)
    combined["clean_text"] = combined["raw_text"].apply(clean_text)
    combined = combined[combined["clean_text"].str.strip() != ""]
    combined = combined.drop_duplicates(subset=["clean_text"]).reset_index(drop=True)
    return combined