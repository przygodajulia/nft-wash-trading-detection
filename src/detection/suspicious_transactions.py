# src/detection/suspicious_transactions.py
import pandas as pd


def get_suspicious_transactions(
    df: pd.DataFrame,
    threshold: int = 30
) -> pd.DataFrame:
    """
    Returns transactions with wash_score greater than or equal to threshold.
    """
    if "wash_score" not in df.columns:
        raise ValueError("Missing required column: wash_score")

    return df[df["wash_score"] >= threshold].copy()


def calculate_suspicious_rate(
    df: pd.DataFrame,
    threshold: int = 30
) -> float:
    """
    Calculates percentage of suspicious transactions.
    """
    if "wash_score" not in df.columns:
        raise ValueError("Missing required column: wash_score")

    if len(df) == 0:
        return 0.0

    suspicious_transactions = get_suspicious_transactions(
        df,
        threshold=threshold
    )

    return len(suspicious_transactions) / len(df) * 100


def calculate_suspicious_rate_per_collection(
    df: pd.DataFrame,
    threshold: int = 30,
    collection_col: str = "nft.collection",
) -> pd.DataFrame:
    """
    Calculates suspicious transaction rate per NFT collection.
    """
    if "wash_score" not in df.columns:
        raise ValueError("Missing required column: wash_score")

    if collection_col not in df.columns:
        raise ValueError(f"Missing required column: {collection_col}")

    result = (
        df.assign(
            is_suspicious=df["wash_score"] >= threshold
        )
        .groupby(collection_col)
        .agg(
            total_transactions=("wash_score", "size"),
            suspicious_transactions=("is_suspicious", "sum"),
        )
        .reset_index()
    )

    result["suspicious_rate"] = (
        result["suspicious_transactions"]
        / result["total_transactions"]
        * 100
    )

    result = result.sort_values(
        "suspicious_rate",
        ascending=False
    )

    return result