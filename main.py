from rism.client import RISMClient


def test_client():
    client = RISMClient()
    query = "Pontio"
    sources = client.search_sources(query=query, rows=20, page=1)

    print(f"Found {len(sources)} sources for query '{query}':")
    for i, source in enumerate(sources, start=1):
        print(f"{i}: {source.title} (composer: {source.composer})")


if __name__ == "__main__":
    test_client()
