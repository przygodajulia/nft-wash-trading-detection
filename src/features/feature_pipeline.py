import pandas as pd

from src.features.base_features import add_base_features
from src.features.self_trading import add_self_trade_feature
from src.features.holding_period import add_holding_period
from src.features.flip_count import add_flip_count
from src.features.wallet_pair import add_wallet_pair_feature
from src.features.circular_trading import add_circular_trading_feature
from src.features.price_anomalies import add_price_anomaly_feature


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Runs the full feature engineering pipeline for NFT wash trading detection.

    The function adds all transaction-level features required
    for later rule-based detection and scoring.
    """
    df = df.copy()

    df = add_base_features(df)
    df = add_self_trade_feature(df)
    df = add_holding_period(df)
    df = add_flip_count(df)
    df = add_wallet_pair_feature(df)
    df = add_circular_trading_feature(df)
    df = add_price_anomaly_feature(df)

    return df