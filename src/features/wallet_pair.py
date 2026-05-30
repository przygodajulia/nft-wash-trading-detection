import pandas as pd


def add_wallet_pair_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates wallet pair transaction frequency.

    The feature represents how many times a given
    seller-buyer pair appears in the dataset.

    Returns:
        DataFrame with:
        - pair_trade_count
    """
    df = df.copy()

    required_columns = [
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

    pair_counts = (
        df.groupby(
            ["seller", "buyer"]
        )
        .size()
        .reset_index(
            name="pair_trade_count"
        )
    )

    df = df.merge(
        pair_counts,
        on=["seller", "buyer"],
        how="left"
    )

    return df