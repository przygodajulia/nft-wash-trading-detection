import pandas as pd


def add_wash_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds rule-based wash trading risk score and risk category.

    The score is based on previously engineered features:
    - self_trade
    - immediate_round_trip
    - pair_trade_count
    - holding_seconds
    - nft_flip_count
    - price_abnormality
    """
    df = df.copy()

    required_columns = [
        "self_trade",
        "immediate_round_trip",
        "pair_trade_count",
        "holding_seconds",
        "nft_flip_count",
        "price_abnormality",
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns for scoring: {missing}"
        )

    df["wash_score"] = (
        df["self_trade"].fillna(False).astype(int) * 35
        + df["immediate_round_trip"].fillna(False).astype(int) * 25
        + (df["pair_trade_count"].fillna(0) >= 5).astype(int) * 15
        + (df["holding_seconds"].fillna(0) <= 3600).astype(int) * 10
        + (df["nft_flip_count"].fillna(0) >= 3).astype(int) * 10
        + df["price_abnormality"].fillna(False).astype(int) * 5
    )

    df["wash_score"] = df["wash_score"].clip(0, 100)

    df["wash_risk"] = df["wash_score"].apply(classify_wash_score)

    return df


def classify_wash_score(score: float) -> str:
    if score >= 70:
        return "High Risk"
    elif score >= 40:
        return "Medium Risk"
    else:
        return "Low Risk"