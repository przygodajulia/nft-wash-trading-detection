import pandas as pd
import json
import os

from src.preprocessing.config import (
    RAW_DIRS,
    PROCESSED_DIR,
    COLLECTIONS,
    RELEVANT_FIELDS,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))
PROCESSED_PATH = os.path.join(REPO_ROOT, PROCESSED_DIR)


def find_json_files(base_dir, collection):
    path = os.path.join(REPO_ROOT, base_dir, collection)
    if not os.path.exists(path):
        return []

    return [
        os.path.join(root, f)
        for root, _, files in os.walk(path)
        for f in files
        if f.lower().endswith(".json")
    ]


def load_collection_json(base_dir, collection):
    rows = []
    for file in find_json_files(base_dir, collection):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            rows.extend(data if isinstance(data, list) else [data])

    if not rows:
        return pd.DataFrame()
    
    return pd.json_normalize(rows, sep=".")


def process_collection(collection):
    print(f"\n📦 Processing {collection}")

    dfs = []
    for raw_dir in RAW_DIRS:
        df = load_collection_json(raw_dir, collection)
        if not df.empty:
            dfs.append(df)

    if not dfs:
        print("⚠️ No data found")
        return

    df = pd.concat(dfs, ignore_index=True)

    existing_fields = [c for c in RELEVANT_FIELDS if c in df.columns]
    df = df[existing_fields].copy()

    df["payment.quantity"] = pd.to_numeric(df["payment.quantity"], errors="coerce")
    df["payment.decimals"] = pd.to_numeric(df["payment.decimals"], errors="coerce")

    df["token_amount"] = (
        df["payment.quantity"] / (10 ** df["payment.decimals"])
    )

    df["event_timestamp"] = pd.to_datetime(
        df["event_timestamp"], unit="s", errors="coerce"
    )
    df["event_day"] = df["event_timestamp"].dt.date

    os.makedirs(PROCESSED_PATH, exist_ok=True)
    out_file = os.path.join(PROCESSED_PATH, f"{collection}_sales.parquet")
    df.to_parquet(out_file, index=False)

    print(f"✅ Saved {len(df)} rows → {out_file}")


def main():
    for collection in COLLECTIONS:
        process_collection(collection)


if __name__ == "__main__":
    main()