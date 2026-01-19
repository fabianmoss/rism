import requests
import time
from pprint import pprint as print

BASE_URL = "http://rism.online"
HEADERS = {"Accept": "application/ld+json"}


def get_source(source_id):
    url = f"{BASE_URL}/sources/{source_id}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def search_sources(q, mode="sources", rows=20):
    params = {"q": q, "mode": mode, "rows": rows}
    url = f"{BASE_URL}/search"
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    query = "Pietro Pontio"
    print(f"Query: {query}")
    time.sleep(1)

    response = search_sources(query)
    print(f"Found {len(response['items'])} entries.")
    time.sleep(1)

    first_entry_id = response["items"][0]["id"].split("/")[-1]
    data = get_source(first_entry_id)
    print(data)
