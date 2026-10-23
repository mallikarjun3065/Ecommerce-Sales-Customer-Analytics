
import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
CLEAN_DIR = BASE_DIR / "data" / "cleaned"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)

# Load orders data
orders = pd.read_csv(
    RAW_DIR / "olist_orders_dataset.csv"
)

print("Original dataset shape:", orders.shape)
print("\nFirst five rows:")
print(orders.head())

print("\nMissing values:")
print(orders.isnull().sum())

print("\nDuplicate order IDs:",
      orders["order_id"].duplicated().sum())

# Convert date columns
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column], errors="coerce"
    )

# Keep one record per order
orders = orders.drop_duplicates(
    subset=["order_id"]
)

# Remove rows without essential identifiers
orders = orders.dropna(
    subset=["order_id", "customer_id"]
)

# Create analysis columns
orders["purchase_year"] = (
    orders["order_purchase_timestamp"].dt.year
)

orders["purchase_month"] = (
    orders["order_purchase_timestamp"].dt.month
)

orders["purchase_year_month"] = (
    orders["order_purchase_timestamp"]
    .dt.to_period("M").astype(str)
)

# Calculate delivery delay in days
orders["delivery_delay_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_estimated_delivery_date"]
).dt.total_seconds() / 86400

# Save cleaned data
orders.to_csv(
    CLEAN_DIR / "orders_cleaned.csv",
    index=False
)

print("\nCleaned dataset shape:", orders.shape)
print("Saved orders_cleaned.csv successfully!")
