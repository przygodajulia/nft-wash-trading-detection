# src/preprocessing/config.py

# Paths
RAW_DIRS = [
    "data/raw/opensea",
]

PROCESSED_DIR = "data/processed/opensea"

# Collections to process
COLLECTIONS = ["boredapeyachtclub", "cryptopunks", "pudgypenguins"]

# Fields to keep for wash trading analysis
RELEVANT_FIELDS = [
    "event_timestamp",
    "closing_date",
    "transaction",           # transaction hash
    "chain",
    "seller",                # seller address
    "buyer",                 # buyer address
    "quantity"
    "nft.identifier",        # token ID
    "nft.name",              # NFT name
    "nft.contract",          # contract address
    "nft.collection",        # collection slug
    "payment.quantity",      # token amount
    "payment.symbol",        # token symbol
    "payment.decimals",       # token decimals
    "payment.token_address"
]

