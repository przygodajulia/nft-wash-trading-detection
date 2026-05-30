import pandas as pd


def add_self_trade_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds self-trade indicator.

    A self-trade occurs when seller and buyer
    addresses are identical.
    """
    df = df.copy()

    required_columns = ["seller", "buyer"]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    df["self_trade"] = (
        df["seller"] == df["buyer"]
    )

    return df