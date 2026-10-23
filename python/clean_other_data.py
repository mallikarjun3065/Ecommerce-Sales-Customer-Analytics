
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
CLEAN_DIR = BASE_DIR / "data" / "cleaned"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)

files = {
    "order_items": "olist_order_items_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv"
}

for table_name, filename in files.items():
    df = pd.read_csv(RAW_DIR / filename)

    print(f"\n{table_name}")
    print("Original shape:", df.shape)
    print("Missing values:\n", df.isnull().sum())

    # Remove exact duplicate rows only
    df = df.drop_duplicates()

    # Convert item prices to numeric values
    if table_name == "order_items":
        df["price"] = pd.to_numeric(
            df["price"], errors="coerce"
        )
        df["freight_value"] = pd.to_numeric(
            df["freight_value"], errors="coerce"
        )

    # Convert payment values
    if table_name == "order_payments":
        df["payment_value"] = pd.to_numeric(
            df["payment_value"], errors="coerce"
        )

    # Save each cleaned table
    df.to_csv(
        CLEAN_DIR / f"{table_name}_cleaned.csv",
        index=False
    )

    print("Cleaned shape:", df.shape)
    print("Saved successfully!")

print("\nAll five tables processed.")
