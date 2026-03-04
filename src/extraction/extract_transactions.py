import os
import json
import logging
from dotenv import load_dotenv

from src.extraction.config import (
    COLLECTION_SLUGS,
    AFTER_TIMESTAMP,
    BEFORE_TIMESTAMP,
    EVENT_TYPES,
    PAGE_LIMIT,
    RAW_DATA_DIR
)
from src.extraction.opensea_client import OpenSeaClient

logging.basicConfig(level=logging.INFO)

def extract_collection(client: OpenSeaClient, collection_slug: str):
    os.makedirs(f"{RAW_DATA_DIR}/{collection_slug}", exist_ok=True)

    cursor = None
    page = 1

    while True:
        events, next_cursor = client.get_events(
            collection_slug=collection_slug,
            after=AFTER_TIMESTAMP,
            before=BEFORE_TIMESTAMP,
            event_types=EVENT_TYPES,
            limit=PAGE_LIMIT,
            cursor=cursor
        )

        if not events:
            logging.info(f"No more events for {collection_slug}")
            break

        output_path = f"{RAW_DATA_DIR}/{collection_slug}/page_{page}.json"
        with open(output_path, "w") as f:
            json.dump(events, f, indent=2)

        logging.info(f"Saved {len(events)} events → {output_path}")

        if not next_cursor:
            break

        cursor = next_cursor
        page += 1


def main():
    load_dotenv()
    api_key = os.getenv("OPENSEA_API_KEY")

    if not api_key:
        raise RuntimeError("Missing OPENSEA_API_KEY in environment")

    client = OpenSeaClient(api_key)

    for collection in COLLECTION_SLUGS:
        logging.info(f"Starting extraction for {collection}")
        extract_collection(client, collection)


if __name__ == "__main__":
    main()