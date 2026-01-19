"""Tests for factory functions."""

import pytest
from rism.models.factory import parse_rism_entry, parse_rism_collection
from rism.models.entities import RISMSource, RISMPerson, RISMInstitution
from rism.models.base import RISMEntry
from rism.models.collections import (
    RISMEntryCollection,
    RISMSourceCollection,
    RISMPersonCollection,
    RISMInstitutionCollection,
)


class TestFactoryFunctions:
    """Test suite for factory functions."""

    def test_parse_rism_entry_source(self, sample_source_data):
        """Test parsing Source entry."""
        entry = parse_rism_entry(sample_source_data)

        assert isinstance(entry, RISMSource)
        assert entry.id == sample_source_data["@id"]
        assert entry.type == "Source"
        assert entry.title == sample_source_data["title"]

    def test_parse_rism_entry_person(self, sample_person_data):
        """Test parsing Person entry."""
        entry = parse_rism_entry(sample_person_data)

        assert isinstance(entry, RISMPerson)
        assert entry.id == sample_person_data["@id"]
        assert entry.type == "Person"
        assert entry.name == sample_person_data["name"]

    def test_parse_rism_entry_institution(self, sample_institution_data):
        """Test parsing Institution entry."""
        entry = parse_rism_entry(sample_institution_data)

        assert isinstance(entry, RISMInstitution)
        assert entry.id == sample_institution_data["@id"]
        assert entry.type == "Institution"
        assert entry.name == sample_institution_data["name"]

    def test_parse_rism_entry_unknown_type(self):
        """Test parsing unknown entry type returns base RISMEntry."""
        unknown_data = {"@id": "test-id", "@type": "UnknownType", "title": "Test Entry"}

        entry = parse_rism_entry(unknown_data)

        assert isinstance(entry, RISMEntry)
        assert not isinstance(entry, (RISMSource, RISMPerson, RISMInstitution))
        assert entry.id == "test-id"
        assert entry.type == "UnknownType"

    def test_parse_rism_entry_case_insensitive(self):
        """Test parsing is case sensitive for type matching."""
        # Lowercase "source" should not match "Source"
        lower_source_data = {
            "@id": "test-source",
            "@type": "source",  # lowercase
            "title": "Test Source",
        }

        entry = parse_rism_entry(lower_source_data)

        # Should return base RISMEntry, not RISMSource
        assert isinstance(entry, RISMEntry)
        assert not isinstance(entry, RISMSource)

    def test_parse_rism_collection_empty(self):
        """Test parsing empty collection."""
        # The factory function currently raises ValueError for empty collections
        # even without raise_if_empty=True due to the collection constraint
        with pytest.raises(ValueError, match="RISMEntryCollection cannot be empty"):
            parse_rism_collection([])

    def test_parse_rism_collection_empty_with_raise(self):
        """Test parsing empty collection with raise_if_empty=True."""
        with pytest.raises(ValueError, match="Empty collection"):
            parse_rism_collection([], raise_if_empty=True)

    def test_parse_rism_collection_type_specific(
        self, sample_source_data, sample_person_data
    ):
        """Test parsing returns type-specific collection."""
        source_data_list = [
            sample_source_data,
            {**sample_source_data, "@id": "test-source-2", "title": "Another Source"},
        ]

        collection = parse_rism_collection(source_data_list)

        assert isinstance(collection, RISMSourceCollection)
        assert len(collection) == 2
        assert collection.entry_type == RISMSource

        # Test all entries are sources
        for entry in collection:
            assert isinstance(entry, RISMSource)

    def test_parse_rism_collection_person_type(self, sample_person_data):
        """Test parsing person collection."""
        person_data_list = [
            sample_person_data,
            {**sample_person_data, "@id": "test-person-2", "name": "Another Person"},
        ]

        collection = parse_rism_collection(person_data_list)

        assert isinstance(collection, RISMPersonCollection)
        assert len(collection) == 2
        assert collection.entry_type == RISMPerson

    def test_parse_rism_collection_institution_type(self, sample_institution_data):
        """Test parsing institution collection."""
        institution_data_list = [
            sample_institution_data,
            {
                **sample_institution_data,
                "@id": "test-institution-2",
                "name": "Another Institution",
            },
        ]

        collection = parse_rism_collection(institution_data_list)

        assert isinstance(collection, RISMInstitutionCollection)
        assert len(collection) == 2
        assert collection.entry_type == RISMInstitution

    def test_parse_rism_collection_mixed_types(self):
        """Test parsing collection with mixed types."""
        mixed_data = [
            {"@id": "test-source", "@type": "Source", "title": "Test Source"},
            {"@id": "test-person", "@type": "Person", "name": "Test Person"},
        ]

        # The factory function will try to create a SourceCollection for the first item
        # but will fail type validation when processing the second item
        with pytest.raises(TypeError, match="All entries must be of the same type"):
            parse_rism_collection(mixed_data)

    def test_parse_rism_collection_unknown_type(self):
        """Test parsing collection with unknown type returns base collection."""
        unknown_data = [
            {"@id": "test-unknown-1", "@type": "UnknownType", "title": "Unknown 1"},
            {"@id": "test-unknown-2", "@type": "UnknownType", "title": "Unknown 2"},
        ]

        collection = parse_rism_collection(unknown_data)

        assert isinstance(collection, RISMEntryCollection)
        assert len(collection) == 2
        assert collection.entry_type == RISMEntry

        # All entries should be base RISMEntry
        for entry in collection:
            assert isinstance(entry, RISMEntry)
            assert not isinstance(entry, (RISMSource, RISMPerson, RISMInstitution))

    def test_parse_rism_collection_single_item(self, sample_source_data):
        """Test parsing collection with single item."""
        collection = parse_rism_collection([sample_source_data])

        assert isinstance(collection, RISMSourceCollection)
        assert len(collection) == 1
        assert collection[0].id == sample_source_data["@id"]

    def test_parse_rism_entry_missing_fields(self):
        """Test parsing entry with missing required fields."""
        minimal_data = {
            "title": "Test Entry"
            # Missing @id and @type
        }

        entry = parse_rism_entry(minimal_data)

        assert isinstance(entry, RISMEntry)
        assert entry.id is None
        assert entry.type is None

    def test_parse_rism_collection_factory_chain(self):
        """Test that factory functions work together in a chain."""
        # Simulate API response data
        api_response_data = [
            {"@id": "source-1", "@type": "Source", "title": "Source 1", "date": "1600"},
            {"@id": "source-2", "@type": "Source", "title": "Source 2", "date": "1650"},
        ]

        # Parse the collection
        collection = parse_rism_collection(api_response_data)

        # Verify it's a source collection
        assert isinstance(collection, RISMSourceCollection)
        assert len(collection) == 2

        # Verify we can access properties
        for entry in collection:
            assert isinstance(entry, RISMSource)
            assert entry.title is not None
            assert entry.date is not None
