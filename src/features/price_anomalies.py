import pandas as pd


def add_price_anomaly_feature(
    df: pd.DataFrame,
    min_trades_per_group: int = 5,
    zscore_threshold: float = 3.5,
) -> pd.DataFrame:
    """
    Adds price anomaly features using robust statistics.

    The method compares NFT transaction prices against
    the median price for a given collection and day.
    Median Absolute Deviation (MAD) is used instead of
    standard deviation to reduce sensitivity to outliers.

    Returns:
        DataFrame with:
        - median_price
        - mad_price
        - n_trades
        - price_zscore
        - price_abnormality
    """
    df = df.copy()

    required_columns = [
        "nft.collection",
        "event_day",
        "token_amount",
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    daily_stats = (
        df.groupby(["nft.collection", "event_day"])
        .agg(
            median_price=("token_amount", "median"),
            mad_price=(
                "token_amount",
                lambda x: (x - x.median()).abs().median(),
            ),
            n_trades=("token_amount", "count"),
        )
        .reset_index()
    )

    reliable_daily_stats = daily_stats[
        daily_stats["n_trades"] >= min_trades_per_group
    ]

    df = df.merge(
        reliable_daily_stats,
        on=["nft.collection", "event_day"],
        how="left",
    )

    df["mad_price"] = (
        df["mad_price"]
        .replace(0, 1e-9)
    )

    df["price_zscore"] = (
        0.6745
        * (df["token_amount"] - df["median_price"])
        / df["mad_price"]
    )

    df["price_abnormality"] = (
        df["price_zscore"].abs()
        > zscore_threshold
    )

    return df