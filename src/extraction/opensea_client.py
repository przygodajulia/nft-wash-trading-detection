import requests
import logging
from typing import Tuple, List, Optional
from requests.exceptions import ConnectionError, Timeout


class OpenSeaClient:
    def __init__(self, api_key: str):
        self.session = requests.Session()
        self.session.headers.update({
            "accept": "application/json",
            "X-API-KEY": api_key
        })

    def get_events(
        self,
        collection_slug: str,
        after: int,
        before: int,
        event_types: List[str],
        limit: int,
        cursor: Optional[str] = None
    ) -> Tuple[List[dict], Optional[str]]:
        """
        Fetch paginated events for a given NFT collection from OpenSea.
        """
        
        params = [
            ("after", after),
            ("before", before),
            ("limit", limit),
        ]

        for event_type in event_types:
            params.append(("event_type", event_type))

        if cursor:
            params.append(("next", cursor))

        url = f"https://api.opensea.io/api/v2/events/collection/{collection_slug}"

        try:
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            events = data.get("asset_events", [])
            next_cursor = data.get("next")

            return events, next_cursor

        except (ConnectionError, Timeout) as e:
            logging.error(f"Connection issue for collection={collection_slug}: {e}")
            return [], None

        except Exception as e:
            logging.error(f"Unexpected error for collection={collection_slug}: {e}")
            return [], None