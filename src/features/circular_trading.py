import pandas as pd


def add_circular_trading_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds circular trading related features.

    The function detects:
    - immediate round-trip patterns (A -> B -> A),
    - repeated seller-buyer interactions for the same NFT.

    Returns:
        DataFrame with:
        - prev_owner
        - immediate_round_trip
        - pair_repeat_count
        - repeated_pair_cycle
        - circular_trading
    """
    df = df.copy()

    required_columns = [
        "nft_id",
        "event_timestamp",
        "seller",
        "buyer",
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

    df = (
        df.sort_values(
            ["nft_id", "event_timestamp"]
        )
        .reset_index(drop=True)
    )

    df["prev_owner"] = (
        df.groupby("nft_id")["seller"]
        .shift(1)
    )

    df["immediate_round_trip"] = (
        df["buyer"] == df["prev_owner"]
    )

    pair_cycle_counts = (
        df.groupby(
            ["nft_id", "seller", "buyer"]
        )
        .size()
        .reset_index(
            name="pair_repeat_count"
        )
    )

    df = df.merge(
        pair_cycle_counts,
        on=["nft_id", "seller", "buyer"],
        how="left"
    )

    df["repeated_pair_cycle"] = (
        df["pair_repeat_count"] >= 2
    )

    df["circular_trading"] = (
        df["immediate_round_trip"]
        | df["repeated_pair_cycle"]
    )

    return df