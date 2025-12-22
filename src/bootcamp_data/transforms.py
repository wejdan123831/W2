import pandas as pd

# convert amount and quantity to float 

def enforce_schema(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(
        order_id=df["order_id"].astype("string"),
        user_id=df["user_id"].astype("string"),
        amount=pd.to_numeric(df["amount"], errors="coerce").astype("Float64"),
        quantity=pd.to_numeric(df["quantity"], errors="coerce").astype("Int64"),
    )
    
# measure missingness per column , (counts + percentages)
def missingness_report(df):
 n = len(df)
 return (
 df.isna().sum()
 .rename("n_missing")
 .to_frame()
 .assign(p_missing=lambda t: t["n_missing"] / n)
 .sort_values("p_missing", ascending=False)
 )
 
def add_missing_flags(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    
    out = df.copy()
    for c in cols:
        out[f"{c}__isna"] = out[c].isna()   # TODO: your code here

    return out

import re
_ws = re.compile(r"\s+")
def normalize_text(s: pd.Series) -> pd.Series:
    return (
        s.astype("string")
        .str.strip()
        .str.casefold()
        .str.replace(_ws, " ", regex=True)
    )
#  return Series with mapped values
def apply_mapping(s: pd.Series, mapping: dict) -> pd.Series:
    return s.map(lambda x: mapping.get(x, x))


# remoove duplicate and keeping the latest row
def dedupe_keep_latest(df, key_cols, ts_col):
 return (
 df.sort_values(ts_col)
 .drop_duplicates(subset=key_cols, keep="last")
 .reset_index(drop=True)
 )
