"""Tests for collection classes."""

import pytest
from rism.models.collections import (
    RISMEntryCollection,
    RISMSourceCollection,
    RISMPersonCollection,
    RISMInstitutionCollection,
)
from rism.models.entities import RISMSource, RISMPerson, RISMInstitution
from rism.models.base import RISMEntry


class TestRISMEntryCollection:
    """Test suite for collection classes."""

    def test_collection_creation(self, sample_source_data):
        """Test collection creation with valid entries."""
        source1 = RISMSource(sample_source_data)
        source2 = RISMSource(
            {**sample_source_data, "@id": "test-source-2", "title": "Another Source"}
        )

        collection = RISMSourceCollection([source1, source2])

        assert len(collection) == 2
        assert collection.entry_type == RISMSource
        assert list(collection) == [source1, source2]

    def test_collection_type_validation(self):
        """Test collection enforces homogeneous entry types."""
        source_data1 = {
            "@id": "test-source-1",
            "@type": "Source",
            "title": "Test Source 1",
        }
        source_data2 = {
            "@id": "test-source-2",
            "@type": "Source",
            "title": "Test Source 2",
        }

        source1 = RISMSource(source_data1)
        source2 = RISMSource(source_data2)

        # This should work - same type
        collection = RISMSourceCollection([source1, source2])
        assert len(collection) == 2

    def test_collection_empty_error(self):
        """Test collection raises error for empty entries."""
        with pytest.raises(ValueError, match="RISMEntryCollection cannot be empty"):
            RISMSourceCollection([])

    def test_collection_iteration(self, sample_source_data):
        """Test collection iteration methods."""
        source1 = RISMSource(sample_source_data)
        source2 = RISMSource({**sample_source_data, "@id": "test-source-2"})

        collection = RISMSourceCollection([source1, source2])

        # Test iteration
        entries = list(collection)
        assert len(entries) == 2
        assert entries[0] == source1
        assert entries[1] == source2

        # Test iteration with for loop
        count = 0
        for entry in collection:
            assert isinstance(entry, RISMSource)
            count += 1
        assert count == 2

    def test_collection_indexing(self, sample_source_data):
        """Test collection indexing and slicing."""
        source1 = RISMSource(sample_source_data)
        source2 = RISMSource({**sample_source_data, "@id": "test-source-2"})
        source3 = RISMSource({**sample_source_data, "@id": "test-source-3"})

        collection = RISMSourceCollection([source1, source2, source3])

        # Test indexing
        assert collection[0] == source1
        assert collection[1] == source2
        assert collection[-1] == source3

        # Test slicing
        first_two = collection[:2]
        assert len(first_two) == 2
        assert first_two[0] == source1
        assert first_two[1] == source2

    def test_collection_ids_method(self, sample_source_data):
        """Test ids method returns list of entry IDs."""
        source1 = RISMSource(sample_source_data)
        source2 = RISMSource(
            {**sample_source_data, "@id": "test-source-2", "title": "Another Source"}
        )

        collection = RISMSourceCollection([source1, source2])

        ids = collection.ids()
        assert len(ids) == 2
        assert sample_source_data["@id"] in ids
        assert "test-source-2" in ids

    def test_collection_to_dicts(self, sample_source_data):
        """Test to_dicts method returns list of dictionaries."""
        source1 = RISMSource(sample_source_data)
        source2 = RISMSource(
            {**sample_source_data, "@id": "test-source-2", "title": "Another Source"}
        )

        collection = RISMSourceCollection([source1, source2])

        dicts = collection.to_dicts()
        assert len(dicts) == 2
        assert dicts[0] == source1.raw
        assert dicts[1] == source2.raw

    def test_collection_len(self, sample_source_data):
        """Test collection length."""
        source1 = RISMSource(sample_source_data)
        source2 = RISMSource({**sample_source_data, "@id": "test-source-2"})

        collection1 = RISMSourceCollection([source1])
        collection2 = RISMSourceCollection([source1, source2])

        assert len(collection1) == 1
        assert len(collection2) == 2

    def test_specific_collection_types(
        self, sample_source_data, sample_person_data, sample_institution_data
    ):
        """Test specific collection types work correctly."""
        source = RISMSource(sample_source_data)
        person = RISMPerson(sample_person_data)
        institution = RISMInstitution(sample_institution_data)

        source_collection = RISMSourceCollection([source])
        person_collection = RISMPersonCollection([person])
        institution_collection = RISMInstitutionCollection([institution])

        # Test inheritance
        assert isinstance(source_collection, RISMEntryCollection)
        assert isinstance(person_collection, RISMEntryCollection)
        assert isinstance(institution_collection, RISMEntryCollection)

        # Test specific types
        assert source_collection.entry_type == RISMSource
        assert person_collection.entry_type == RISMPerson
        assert institution_collection.entry_type == RISMInstitution

    def test_collection_with_base_entries(self):
        """Test collection type constraints."""
        # Create valid source entries
        source_data = {"@id": "test-source", "@type": "Source", "title": "Test Source"}
        source1 = RISMSource(source_data)
        source2 = RISMSource({**source_data, "@id": "test-source-2"})

        # This should work
        collection = RISMSourceCollection([source1, source2])
        assert len(collection) == 2
        assert collection.entry_type == RISMSource

        ids = collection.ids()
        assert len(ids) == 2
        assert "test-source" in ids
        assert "test-source-2" in ids
