import json
import os

import pandas as pd

from src.preprocessing.config import (
    RAW_DIRS,
    PROCESSED_DIR,
    COLLECTIONS,
    RELEVANT_FIELDS,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))
PROCESSED_PATH = os.path.join(REPO_ROOT, PROCESSED_DIR)


def find_json_files(base_dir: str, collection: str) -> list[str]:
    """
    Searches recursively for JSON files belonging to a specific NFT collection.

    Parameters
    ----------
    base_dir : str
        Base directory containing raw extraction results.
    collection : str
        NFT collection slug.

    Returns
    -------
    list[str]
        List of paths to JSON files found for the selected collection.
        Returns an empty list if the directory does not exist.
    """
    path = os.path.join(REPO_ROOT, base_dir, collection)

    if not os.path.exists(path):
        return []

    return [
        os.path.join(root, file_name)
        for root, _, files in os.walk(path)
        for file_name in files
        if file_name.lower().endswith(".json")
    ]


def load_collection_json(base_dir: str, collection: str) -> pd.DataFrame:
    """
    Loads all JSON files for a given NFT collection and converts them into
    a normalized pandas DataFrame.

    The function combines data from multiple paginated API response files
    into a single tabular dataset.

    Parameters
    ----------
    base_dir : str
        Directory containing raw extraction results.
    collection : str
        NFT collection slug.

    Returns
    -------
    pandas.DataFrame
        Normalized DataFrame containing all records found for the collection.
        Returns an empty DataFrame if no data is available.
    """
    rows = []

    for file_path in find_json_files(base_dir, collection):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                rows.extend(data)
            else:
                rows.append(data)

    if not rows:
        return pd.DataFrame()

    return pd.json_normalize(rows, sep=".")


def process_collection(collection: str) -> None:
    """
    Processes raw OpenSea event data for a single NFT collection.

    The function loads all extracted JSON files, merges them into a single
    dataset, selects relevant fields, performs basic transformations,
    calculates token amounts, converts timestamps, and saves the result
    as a Parquet file.

    Parameters
    ----------
    collection : str
        NFT collection slug to process.

    Returns
    -------
    None
        The processed dataset is written to disk as a Parquet file.
    """
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

    existing_fields = [
        column
        for column in RELEVANT_FIELDS
        if column in df.columns
    ]

    df = df[existing_fields].copy()

    df["payment.quantity"] = pd.to_numeric(
        df["payment.quantity"],
        errors="coerce"
    )

    df["payment.decimals"] = pd.to_numeric(
        df["payment.decimals"],
        errors="coerce"
    )

    df["token_amount"] = (
        df["payment.quantity"] /
        (10 ** df["payment.decimals"])
    )

    df["event_timestamp"] = pd.to_datetime(
        df["event_timestamp"],
        unit="s",
        errors="coerce"
    )

    df["event_day"] = df["event_timestamp"].dt.date

    os.makedirs(PROCESSED_PATH, exist_ok=True)

    output_file = os.path.join(
        PROCESSED_PATH,
        f"{collection}_sales.parquet"
    )

    df.to_parquet(output_file, index=False)

    print(f"✅ Saved {len(df)} rows → {output_file}")


def main() -> None:
    """
    Runs the preprocessing pipeline for all configured NFT collections.

    The function iterates through the collection list defined in the
    preprocessing configuration and generates processed Parquet datasets
    for each collection.

    Returns
    -------
    None
    """
    for collection in COLLECTIONS:
        process_collection(collection)


if __name__ == "__main__":
    main()