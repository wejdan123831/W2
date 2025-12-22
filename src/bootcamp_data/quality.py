
import pandas as pd

def require_columns(df, cols):
 missing = [c for c in cols if c not in df.columns]
 assert not missing, f"Missing columns: {missing}"
 
def assert_non_empty(df, name="df"):
 assert len(df) > 0, f"{name} has 0 rows"

def assert_unique_key(df, key, allow_na=False):
 if not allow_na:
     assert df[key].notna().all(), f"{key} contains NA"
 dup = df[key].duplicated(keep=False) & df[key].notna()
 assert not dup.any(), f"{key} not unique; {dup.sum()} duplicate rows"
 
def assert_in_range(s, lo=None, hi=None, name="value"):
    x = s.dropna()
    if lo is not None:
         assert (x >= lo).all(), f"{name} below {lo}"
    if hi is not None:
         assert (x <= hi).all(), f"{name} above {hi}"