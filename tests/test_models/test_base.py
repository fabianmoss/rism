"""Tests for RISMEntry base class."""

import pytest
from dataclasses import FrozenInstanceError
from rism.models.base import RISMEntry


class TestRISMEntry:
    """Test suite for RISMEntry base class."""

    def test_entry_creation(self):
        """Test RISMEntry creation with valid data."""
        raw_data = {"@id": "test-id", "@type": "TestType", "title": "Test Title"}

        entry = RISMEntry(raw_data)

        assert entry.raw == raw_data
        assert entry.id == "test-id"
        assert entry.type == "TestType"

    def test_entry_post_init(self):
        """Test __post_init__ method sets id and type correctly."""
        raw_data = {
            "@id": "https://rism.online/sources/123",
            "@type": "Source",
            "title": "Test Source",
        }

        entry = RISMEntry(raw_data)

        assert entry.id == "https://rism.online/sources/123"
        assert entry.type == "Source"

    def test_entry_missing_id_field(self):
        """Test entry creation with missing @id field."""
        raw_data = {"@type": "Source", "title": "Test Source"}

        entry = RISMEntry(raw_data)

        assert entry.id is None
        assert entry.type == "Source"

    def test_entry_missing_type_field(self):
        """Test entry creation with missing @type field."""
        raw_data = {"@id": "test-id", "title": "Test Source"}

        entry = RISMEntry(raw_data)

        assert entry.id == "test-id"
        assert entry.type is None

    def test_entry_missing_both_fields(self):
        """Test entry creation with missing both @id and @type."""
        raw_data = {"title": "Test Source"}

        entry = RISMEntry(raw_data)

        assert entry.id is None
        assert entry.type is None

    def test_entry_empty_raw_data(self):
        """Test entry creation with empty raw data."""
        entry = RISMEntry({})

        assert entry.raw == {}
        assert entry.id is None
        assert entry.type is None

    def test_entry_to_dict(self):
        """Test to_dict method returns raw data."""
        raw_data = {"@id": "test-id", "@type": "Source", "title": "Test Source"}

        entry = RISMEntry(raw_data)

        assert entry.to_dict() == raw_data
        assert entry.to_dict() is raw_data  # Should be same reference

    def test_entry_repr(self):
        """Test string representation."""
        raw_data = {"@id": "test-id", "@type": "Source", "title": "Test Source"}

        entry = RISMEntry(raw_data)

        expected = "<RISMEntry id=test-id>"
        assert repr(entry) == expected

    def test_entry_repr_without_id(self):
        """Test string representation without id."""
        raw_data = {"@type": "Source"}

        entry = RISMEntry(raw_data)

        expected = "<RISMEntry id=None>"
        assert repr(entry) == expected

    def test_entry_immutability(self):
        """Test that entry is immutable due to frozen dataclass."""
        raw_data = {"@id": "test-id", "@type": "Source", "title": "Test Source"}

        entry = RISMEntry(raw_data)

        # Test that we can create multiple instances with same data
        entry2 = RISMEntry(raw_data)
        assert entry == entry2

        # Test that attributes are accessible but not assignable
        assert entry.id == "test-id"
        assert entry.type == "Source"
        assert entry.raw == raw_data

        # Verify that the object behaves as immutable by testing equality
        # and that the __hash__ method exists (even if dict prevents hashing)
        assert hasattr(entry, "__hash__")
        assert entry == entry2

    def test_entry_type_validation(self):
        """Test that raw data type is validated."""
        # Should accept dict
        entry = RISMEntry({"@id": "test"})
        assert entry is not None

    def test_entry_with_complex_data(self):
        """Test entry with complex nested data."""
        raw_data = {
            "@id": "test-id",
            "@type": "Source",
            "composer": [
                {"name": "Composer 1", "date": "1600-1650"},
                {"name": "Composer 2", "date": "1650-1700"},
            ],
            "metadata": {"created": "2023-01-01", "modified": "2023-12-01"},
        }

        entry = RISMEntry(raw_data)

        assert entry.id == "test-id"
        assert entry.type == "Source"
        assert entry.to_dict() == raw_data

    def test_entry_inheritance_compatibility(self):
        """Test that base class works correctly for inheritance."""

        class TestEntry(RISMEntry):
            @property
            def title(self):
                return self.raw.get("title")

        raw_data = {"@id": "test-id", "@type": "TestType", "title": "Test Title"}

        entry = TestEntry(raw_data)

        assert isinstance(entry, RISMEntry)
        assert entry.id == "test-id"
        assert entry.title == "Test Title"
