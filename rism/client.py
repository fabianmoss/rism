from typing import List
from dataclasses import dataclass
import requests

BASE_URL = "https://rism.online"
HEADERS = {"Accept": "application/ld-json"}


@dataclass
class RISMSource:
    id: str
    title: str
    composer: str = None


class RISMClient:
    """Minimal client to query RISM sources."""

    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def search_sources(
        self, query: str, rows: int = 20, page: int = 1
    ) -> List[RISMSource]:
        """Search sources and return a list of RISMSource dataclasses."""
        url = f"{self.base_url}/search"
        params = {"q": query, "mode": "sources", "rows": rows, "page": page}

        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        items = data.get("items", [])
        sources = []
        for item in items:
            sources.append(
                RISMSource(
                    id=item.get("id"),
                    title=item.get("title", "No title"),
                    composer=item.get("composer"),
                )
            )
        return sources
