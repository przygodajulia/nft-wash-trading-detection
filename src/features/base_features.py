import pandas as pd


def add_base_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds base columns required for NFT transaction feature engineering.
    """
    df = df.copy()

    df["event_timestamp"] = pd.to_datetime(df["event_timestamp"], utc=True)
    df["event_day"] = df["event_timestamp"].dt.date

    df["nft_id"] = (
        df["nft.contract"].astype(str)
        + "_"
        + df["nft.name"].astype(str)
    )

    df = df.sort_values(["nft_id", "event_timestamp"]).reset_index(drop=True)

    return df