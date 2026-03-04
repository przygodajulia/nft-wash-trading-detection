import pandas as pd
import json
import os

# Config
from src.preprocessing.config import RAW_DIRS as RAW_DIRS_CONFIG, PROCESSED_DIR as PROCESSED_DIR_CONFIG, COLLECTIONS, RELEVANT_FIELDS

# Absolute path to processed folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # src/preprocessing
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))
PROCESSED_DIR = os.path.join(REPO_ROOT, PROCESSED_DIR_CONFIG)

# -----------------------------
# Helper functions
# -----------------------------
def find_json_files(folder_path, collection_slug):
    """Recursively find all .json files in a folder (case-insensitive)"""
    full_path = os.path.join(REPO_ROOT, folder_path, collection_slug)
    print(f"Looking in: {full_path}")
    if not os.path.exists(full_path):
        print(f"⚠️ Folder does not exist: {full_path}")
        return []

    json_files = []
    for root, _, files in os.walk(full_path):
        for f in files:
            if f.lower().endswith(".json"):
                json_files.append(os.path.join(root, f))
    print(f"✅ Found {len(json_files)} JSON files in {collection_slug}")
    return json_files

def load_collection_json(folder_path, collection_slug):
    """Load all JSON files for a collection into a flattened DataFrame"""
    files = find_json_files(folder_path, collection_slug)
    data_list = []
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                data_list.extend(data)
            else:
                data_list.append(data)

    if not data_list:
        return pd.DataFrame()

    # Flatten nested dictionaries
    df = pd.json_normalize(data_list, sep="_")
    print(f"📊 DataFrame created with {len(df)} rows from {collection_slug}")
    return df

def unpack_bundles(df):
    """For bundle events, create one row per NFT, keeping is_bundle=True"""
    rows = []
    for _, row in df.iterrows():
        if "asset_bundle_assets" in row and pd.notna(row["asset_bundle_assets"]):
            assets = row["asset_bundle_assets"]
            if isinstance(assets, list):
                for nft in assets:
                    new_row = row.copy()
                    new_row["asset_identifier"] = nft.get("identifier", None)
                    new_row["asset_name"] = nft.get("name", None)
                    new_row["asset_contract"] = nft.get("contract", row.get("asset_contract"))
                    new_row["asset_collection"] = nft.get("collection", row.get("asset_collection"))
                    new_row["is_bundle"] = True
                    rows.append(new_row)
            else:
                row["is_bundle"] = True
                rows.append(row)
        else:
            row["is_bundle"] = False
            rows.append(row)
    return pd.DataFrame(rows)

# -----------------------------
# Main processing
# -----------------------------
def process_collection(collection):
    print(f"\nProcessing {collection}...")
    dfs = []
    for raw_dir in RAW_DIRS_CONFIG:
        df = load_collection_json(raw_dir, collection)
        if not df.empty:
            dfs.append(df)
    if not dfs:
        print(f"No data found for {collection}. Skipping.")
        return

    df = pd.concat(dfs, ignore_index=True)

    # Flatten nested fields done via json_normalize already

    # Keep only relevant fields that exist
    existing_fields = [f for f in RELEVANT_FIELDS if f in df.columns]
    df_clean = df[existing_fields].copy()

    # Token amount calculation
    if "payment_quantity" in df_clean.columns and "payment_decimals" in df_clean.columns:
        df_clean["quantity"] = pd.to_numeric(df_clean["payment_quantity"], errors="coerce")
        df_clean["decimals"] = pd.to_numeric(df_clean["payment_decimals"], errors="coerce")
        df_clean["token_amount"] = df_clean["quantity"] / (10 ** df_clean["decimals"])
    else:
        df_clean["token_amount"] = None

    # Timestamp conversion
    if "event_timestamp" in df_clean.columns:
        df_clean["event_timestamp"] = pd.to_datetime(df_clean["event_timestamp"], unit="s", errors="coerce")
        df_clean["event_day"] = df_clean["event_timestamp"].dt.date

    # Unpack bundles
    df_clean = unpack_bundles(df_clean)

    # Only successful sales
    if "event_type" in df_clean.columns:
        df_sales = df_clean[df_clean["event_type"] == "successful"].copy()
    else:
        df_sales = df_clean.copy()

    # Final columns to keep
    final_cols = [
        "event_type", "event_timestamp", "event_day", "transaction_transaction_hash", "chain",
        "from_address", "to_address", "asset_identifier", "asset_name", "asset_contract", "asset_collection",
        "payment_symbol", "token_amount", "is_bundle"
    ]
    # Keep only existing columns
    final_cols_existing = [c for c in final_cols if c in df_sales.columns]
    df_sales = df_sales[final_cols_existing]

    # Save Parquet
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    output_file = os.path.join(PROCESSED_DIR, f"{collection}_sales.parquet")
    df_sales.to_parquet(output_file, index=False)
    print(f"💾 Saved processed data to {output_file}")

# -----------------------------
# Main
# -----------------------------
def main():
    for collection in COLLECTIONS:
        process_collection(collection)

if __name__ == "__main__":
    main()