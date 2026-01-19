"""Tests for RISMClient class."""

import pytest
import responses
from rism.client import RISMClient
from tests.fixtures.sample_responses import (
    SAMPLE_SOURCE_SEARCH,
    SAMPLE_EMPTY_SEARCH,
    ERROR_RESPONSES,
)


class TestRISMClient:
    """Test suite for RISMClient class."""

    def test_client_initialization(self, rism_client):
        """Test client initialization and configuration."""
        assert rism_client.base_url == "https://rism.online"
        assert rism_client.session is not None
        assert "Accept" in rism_client.session.headers
        assert rism_client.session.headers["Accept"] == "application/ld-json"

    def test_client_has_correct_base_url(self):
        """Test client uses correct base URL."""
        client = RISMClient()
        assert client.base_url == "https://rism.online"

    def test_client_session_configuration(self):
        """Test client session is properly configured."""
        client = RISMClient()
        assert hasattr(client, "session")
        # Session headers is a case-insensitive dict-like object
        assert client.session.headers is not None
        assert "Accept" in client.session.headers

    def test_search_sources_success(self, rism_client):
        """Test successful source search."""
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                "https://rism.online/search",
                json=SAMPLE_SOURCE_SEARCH,
                status=200,
            )

            sources = rism_client.search_sources(query="test", rows=20, page=1)

            assert len(sources) == 1
            source = sources[0]
            assert source.id == "https://rism.online/sources/123456"
            assert source.title == "Test Source"
            assert source.composer == [{"name": "Test Composer", "date": "1550-1620"}]

    def test_search_sources_empty_result(self, rism_client):
        """Test search with no results."""
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                "https://rism.online/search",
                json=SAMPLE_EMPTY_SEARCH,
                status=200,
            )

            sources = rism_client.search_sources(query="nonexistent")

            assert len(sources) == 0

    def test_search_sources_default_parameters(self, rism_client):
        """Test search with default parameters."""
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                "https://rism.online/search",
                json=SAMPLE_EMPTY_SEARCH,
                status=200,
            )

            rism_client.search_sources(query="test")

            # Check that default parameters were used
            assert len(rsps.calls) == 1
            request = rsps.calls[0].request
            request_url = str(request.url)
            assert "q=test" in request_url
            assert "rows=20" in request_url
            assert "page=1" in request_url

    def test_search_sources_custom_parameters(self, rism_client):
        """Test search with custom parameters."""
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                "https://rism.online/search",
                json=SAMPLE_SOURCE_SEARCH,
                status=200,
            )

            sources = rism_client.search_sources(query="test", rows=40, page=2)

            assert len(sources) == 1

    def test_search_sources_http_error(self, rism_client):
        """Test handling of HTTP errors."""
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                "https://rism.online/search",
                json=ERROR_RESPONSES["invalid_page_size"],
                status=400,
            )

            with pytest.raises(Exception):  # Should raise an HTTP error
                rism_client.search_sources(query="test", rows=999)  # Invalid page size

    def test_search_sources_missing_items(self, rism_client):
        """Test handling of response without items array."""
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                "https://rism.online/search",
                json={"malformed": "response"},
                status=200,
            )

            sources = rism_client.search_sources(query="test")

            assert sources == []  # Should gracefully handle missing items

    def test_search_sources_malformed_items(self, rism_client):
        """Test handling of malformed item data."""
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                "https://rism.online/search",
                json={"items": [{"id": None, "title": None}]},
                status=200,
            )

            sources = rism_client.search_sources(query="test")

            # Should handle missing fields gracefully
            assert len(sources) == 1
            assert sources[0].id is None
            # Note: .get("title", "No title") returns "No title" only if title is missing,
            # not if title is explicitly None. So the title will be None here.
            assert sources[0].title is None  # Explicit None value
            assert sources[0].composer is None  # Default for missing fields

    @pytest.mark.parametrize(
        "query,rows,page",
        [
            ("test", 20, 1),
            ("", 40, 2),
            ("special chars!@#$%^&*()", 100, 3),
            ("unicode: ♪♫♬", 20, 1),
        ],
    )
    def test_search_sources_various_queries(self, rism_client, query, rows, page):
        """Test search with various query types."""
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                "https://rism.online/search",
                json=SAMPLE_EMPTY_SEARCH,
                status=200,
            )

            sources = rism_client.search_sources(query=query, rows=rows, page=page)

            # Should not raise any exceptions
            assert isinstance(sources, list)
            assert len(rsps.calls) == 1

    def test_search_sources_parameter_types(self, rism_client):
        """Test parameter type validation."""
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                "https://rism.online/search",
                json=SAMPLE_EMPTY_SEARCH,
                status=200,
            )

            # All parameter types should work
            sources = rism_client.search_sources(query="test", rows=20, page=1)

            assert isinstance(sources, list)

    @pytest.mark.slow
    @pytest.mark.api
    def test_search_sources_integration(self, rism_client):
        """Integration test with real API (marked as slow)."""
        pytest.skip("Integration tests disabled by default")
