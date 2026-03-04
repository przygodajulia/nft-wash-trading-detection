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
    "event_type",
    "event_timestamp",
    "transaction",           # transaction hash
    "chain",
    "seller",                # seller address
    "buyer",                 # buyer address
    "from_address",          # for transfer events
    "to_address",            # for transfer events
    "transfer_type",         # for transfer events
    "nft.identifier",        # token ID
    "nft.name",              # NFT name
    "nft.contract",          # contract address
    "nft.collection",        # collection slug
    "payment.quantity",      # token amount
    "payment.symbol",        # token symbol
    "payment.decimals"       # token decimals
]

