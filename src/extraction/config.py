# Contains parameters needed for data extraction
from datetime import datetime

# Collections analyzed in the thesis
COLLECTION_SLUGS = [
    "cryptopunks",
    "pudgypenguins",
    "boredapeyachtclub"
]

# Time range (Unix timestamps) - include 3 months time range
AFTER_TIMESTAMP = int(datetime(2025, 7, 1).timestamp())
BEFORE_TIMESTAMP = int(datetime(2025, 9, 30).timestamp())

# API
BASE_URL = "https://api.opensea.io/api/v2/events/collection"
EVENT_TYPES = ["sale"]
PAGE_LIMIT = 50

# Output
RAW_DATA_DIR = "data/raw/opensea"