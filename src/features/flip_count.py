import pandas as pd


def add_flip_count(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates NFT transaction frequency.

    The feature represents how many times a given NFT
    appears in the transaction dataset.

    Returns:
        DataFrame with:
        - nft_flip_count
    """
    df = df.copy()

    required_columns = [
        "nft_id"
    ]

    missing = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    flip_counts = (
        df.groupby("nft_id")
          .size()
    )

    df["nft_flip_count"] = (
        df["nft_id"]
        .map(flip_counts)
    )

    return df