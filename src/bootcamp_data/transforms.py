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

  

def parse_datetime(df: pd.DataFrame, col: str, *, utc: bool = True) -> pd.DataFrame:
    
  
    df = df.copy()
    
  
    df[col] = pd.to_datetime(df[col], errors='coerce', utc=utc)
    
    return df

import pandas as pd


def iqr_bounds(s: pd.Series, k: float = 1.5) -> tuple[float, float]:

    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    return float(q1 - k * iqr), float(q3 + k * iqr)

def add_time_parts(df: pd.DataFrame, ts_col: str) -> pd.DataFrame:
    
    ts = df[ts_col]
    return df.assign(
        date=ts.dt.date,
        year=ts.dt.year,
        month=ts.dt.to_period("M").astype("string"),
        dow=ts.dt.day_name(),
        hour=ts.dt.hour,
    )
def winsorize(s: pd.Series, lo: float = 0.01, hi: float = 0.99) -> pd.Series:
    
    x = s.dropna()
    a, b = x.quantile(lo), x.quantile(hi)
    return s.clip(lower=a, upper=b)

def add_outlier_flag(df: pd.DataFrame, col: str, *, k: float = 1.5) -> pd.DataFrame:
   
    lo, hi = iqr_bounds(df[col], k=k)
    return df.assign(**{f"{col}__is_outlier": (df[col] < lo) | (df[col] > hi)})