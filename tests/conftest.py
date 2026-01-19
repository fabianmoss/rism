"""Pytest configuration and fixtures for RISM tests."""

import pytest
import responses
from typing import Dict, Any
from rism.client import RISMClient


@pytest.fixture
def rism_client():
    """Create a RISMClient instance for testing."""
    return RISMClient()


@pytest.fixture
def sample_search_response():
    """Sample RISM API search response."""
    return {
        "id": "https://rism.online/search?q=Pontio&mode=sources&rows=20",
        "type": "Collection",
        "totalItems": 60,
        "view": {
            "type": "PartialCollectionView",
            "first": "https://rism.online/search?mode=sources&q=Pontio&rows=20",
            "thisPage": 1,
            "totalPages": 3,
        },
        "items": [
            {
                "id": "https://rism.online/sources/990052491",
                "type": "rism:Source",
                "title": "Modulationum cum quinque vocibus, liber 2",
                "composer": [{"name": "Pontio, Pietro", "date": "1532-1596"}],
                "date": "1588",
                "@id": "https://rism.online/sources/990052491",
                "@type": "Source",
            }
        ],
    }


@pytest.fixture
def sample_source_data():
    """Sample source data for domain model testing."""
    return {
        "id": "https://rism.online/sources/990052491",
        "@id": "https://rism.online/sources/990052491",
        "@type": "Source",
        "type": "rism:Source",
        "title": "Modulationum cum quinque vocibus, liber 2",
        "date": "1588",
        "composer": [{"name": "Pontio, Pietro", "date": "1532-1596"}],
        "siglum": "US-NY",
    }


@pytest.fixture
def sample_person_data():
    """Sample person data for domain model testing."""
    return {
        "id": "https://rism.online/people/123456",
        "@id": "https://rism.online/people/123456",
        "@type": "Person",
        "type": "rism:Person",
        "name": "Pontio, Pietro",
        "date": "1532-1596",
        "role": ["composer"],
    }


@pytest.fixture
def sample_institution_data():
    """Sample institution data for domain model testing."""
    return {
        "id": "https://rism.online/institutions/789",
        "@id": "https://rism.online/institutions/789",
        "@type": "Institution",
        "type": "rism:Institution",
        "name": "Bibliothèque Nationale",
        "siglum": "F-Pn",
        "country": "France",
    }


@pytest.fixture
def mock_api_responses():
    """Mock responses for common API calls."""
    with responses.RequestsMock() as rsps:
        yield rsps
