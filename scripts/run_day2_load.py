import logging
import sys
import re
import pandas as pd
from pathlib import Path
from io import StringIO

# import  function we need 

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bootcamp_data.config import make_paths
from bootcamp_data.io import read_orders_csv, read_users_csv, write_parquet
from bootcamp_data.quality import (
    require_columns,
    assert_non_empty,
    assert_in_range,
    assert_unique_key
)
from bootcamp_data.transforms import (
    enforce_schema,
    missingness_report,
    add_missing_flags,
    normalize_text,
    apply_mapping
)

# loging 
logging.basicConfig(
    level=logging.INFO, 
    format="%(levelname)s %(name)s: %(message)s"
)
log = logging.getLogger(__name__)


ROOT = Path(".") 

def main() -> None:
    p = make_paths(ROOT)
    
    log.info("Loading raw inputs")
    # download csv files 
    orders_raw = read_orders_csv(p.raw / "orders.csv")
    users = read_users_csv(p.raw / "users.csv")
    
    log.info("Rows: orders_raw=%s, users=%s", len(orders_raw), len(users))

    # check if any column is missing 
    require_columns(orders_raw, ["order_id", "user_id", "amount", "quantity", "created_at", "status"])
    require_columns(users, ["user_id", "country", "signup_date"])
    
    # check for empty rows
    assert_non_empty(orders_raw, "orders_raw")
    assert_non_empty(users, "users")

    # convert amount and quantity to float 
    orders = enforce_schema(orders_raw)
    
    
    # missing values report 
    rep = missingness_report(orders)
    reports_dir = ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    rep_path = reports_dir / "missingness_orders.csv"
    rep.to_csv(rep_path, index=True)
    log.info("Wrote missingness report: %s", rep_path)

    
    status_norm = normalize_text(orders["status"])
    mapping = {"paid": "paid", "refund": "refund", "refunded": "refund"}
    status_clean = apply_mapping(status_norm, mapping)

    
    orders_clean = (
        orders.assign(status_clean=status_clean)
        .pipe(add_missing_flags, cols=["amount", "quantity"])
    )

   
    assert_in_range(orders_clean["amount"], lo=0, name="order_amount")
    assert_in_range(orders_clean["quantity"], lo=0, name="order_quantity")

    
    write_parquet(orders_clean, p.processed / "orders_clean.parquet")
    write_parquet(users, p.processed / "users.parquet")
    
    log.info("Wrote processed outputs: %s", p.processed)

if __name__ == "__main__":
    main()