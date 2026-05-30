import pandas as pd


def add_holding_period(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates holding period for each NFT.

    Holding period is defined as the time difference between
    the current transaction and the previous transaction
    of the same NFT.

    Returns:
        DataFrame with:
        - prev_sale_time
        - holding_seconds
    """
    df = df.copy()

    required_columns = [
        "nft_id",
        "event_timestamp",
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    df = (
        df.sort_values(["nft_id", "event_timestamp"])
        .reset_index(drop=True)
    )

    df["prev_sale_time"] = (
        df.groupby("nft_id")["event_timestamp"]
        .shift(1)
    )

    df["holding_seconds"] = (
        df["event_timestamp"] - df["prev_sale_time"]
    ).dt.total_seconds()

    return df