"""Sample API responses for testing."""

SAMPLE_SOURCE_SEARCH = {
    "id": "https://rism.online/search?q=test&mode=sources&rows=20",
    "type": "Collection",
    "totalItems": 1,
    "view": {"type": "PartialCollectionView", "thisPage": 1, "totalPages": 1},
    "items": [
        {
            "id": "https://rism.online/sources/123456",
            "@id": "https://rism.online/sources/123456",
            "@type": "Source",
            "type": "rism:Source",
            "title": "Test Source",
            "date": "1600",
            "composer": [{"name": "Test Composer", "date": "1550-1620"}],
        }
    ],
}

SAMPLE_PERSON_SEARCH = {
    "id": "https://rism.online/search?q=test&mode=people&rows=20",
    "type": "Collection",
    "totalItems": 1,
    "items": [
        {
            "id": "https://rism.online/people/123456",
            "@id": "https://rism.online/people/123456",
            "@type": "Person",
            "type": "rism:Person",
            "name": "Test Person",
            "date": "1550-1620",
            "role": ["composer"],
        }
    ],
}

SAMPLE_EMPTY_SEARCH = {
    "id": "https://rism.online/search?q=nonexistent&mode=sources&rows=20",
    "type": "Collection",
    "totalItems": 0,
    "view": {"type": "PartialCollectionView", "thisPage": 1, "totalPages": 0},
    "items": [],
}

ERROR_RESPONSES = {
    "invalid_page_size": {
        "message": "Invalid search query. Invalid value for page size. Only 20, 40, 100 are acceptable values"
    },
    "not_found": {"message": "Resource not found"},
    "server_error": {"message": "Internal server error"},
}
