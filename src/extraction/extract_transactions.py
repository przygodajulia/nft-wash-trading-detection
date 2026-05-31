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


def extract_collection(client: OpenSeaClient, collection_slug: str) -> None:
    """
    Extracts NFT event data for a single OpenSea collection and saves the
    paginated API responses as JSON files.

    The function requests events for the selected collection within the time
    range defined in the extraction configuration. It follows OpenSea pagination
    using the cursor returned by the API and stores each page of results in a
    separate JSON file.

    Parameters
    ----------
    client : OpenSeaClient
        Initialized OpenSea API client used to request collection events.
    collection_slug : str
        OpenSea collection slug identifying the NFT collection to extract.

    Returns
    -------
    None
        The function saves extracted event data to disk and does not return
        any value.
    """
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


def main() -> None:
    """
    Runs the OpenSea data extraction process for all configured NFT collections.

    The function loads environment variables from the `.env` file, retrieves the
    OpenSea API key, initializes the API client, and iterates over all collection
    slugs defined in the extraction configuration.

    Raises
    ------
    RuntimeError
        If the `OPENSEA_API_KEY` variable is missing from the environment.

    Returns
    -------
    None
        The function coordinates the extraction process and saves results to
        disk through `extract_collection`.
    """
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