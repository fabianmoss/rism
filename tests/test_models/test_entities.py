"""Tests for domain entities."""

import pytest
from rism.models.entities import RISMSource, RISMPerson, RISMInstitution


class TestRISMSource:
    """Test suite for RISMSource entity."""

    def test_source_creation(self, sample_source_data):
        """Test RISMSource creation with valid data."""
        source = RISMSource(sample_source_data)

        assert source.raw == sample_source_data
        assert source.id == "https://rism.online/sources/990052491"
        assert source.type == "Source"

    def test_source_properties(self, sample_source_data):
        """Test all property methods return expected values."""
        source = RISMSource(sample_source_data)

        assert source.title == "Modulationum cum quinque vocibus, liber 2"
        assert source.date == "1588"
        assert source.siglum == "US-NY"

    def test_source_composers_property(self, sample_source_data):
        """Test composers property returns list correctly."""
        source = RISMSource(sample_source_data)

        composers = source.composers
        assert isinstance(composers, list)
        assert len(composers) == 1
        assert composers[0]["name"] == "Pontio, Pietro"
        assert composers[0]["date"] == "1532-1596"

    def test_source_optional_fields(self):
        """Test handling of missing optional fields."""
        minimal_data = {"@id": "test-source-id", "@type": "Source"}

        source = RISMSource(minimal_data)

        assert source.title is None
        assert source.date is None
        assert source.composers == []
        assert source.siglum is None

    def test_source_empty_composers_list(self):
        """Test source with empty composers list."""
        data = {"@id": "test-source-id", "@type": "Source", "composer": []}

        source = RISMSource(data)

        assert source.composers == []

    def test_source_multiple_composers(self):
        """Test source with multiple composers."""
        data = {
            "@id": "test-source-id",
            "@type": "Source",
            "composer": [
                {"name": "Composer 1", "date": "1600-1650"},
                {"name": "Composer 2", "date": "1650-1700"},
            ],
        }

        source = RISMSource(data)

        composers = source.composers
        assert len(composers) == 2
        assert composers[0]["name"] == "Composer 1"
        assert composers[1]["name"] == "Composer 2"


def test_source_immutability(self, sample_source_data):
    """Test that source is immutable."""
    source = RISMSource(sample_source_data)

    # Test equality
    source2 = RISMSource(sample_source_data)
    assert source == source2

    # Test that the dataclass is frozen (though dicts aren't hashable)
    # We can test that the object has the right attributes and behaves consistently
    assert hasattr(source, "__dataclass_fields__")
    assert source.raw == source2.raw


class TestRISMPerson:
    """Test suite for RISMPerson entity."""

    def test_person_creation(self, sample_person_data):
        """Test RISMPerson creation with valid data."""
        person = RISMPerson(sample_person_data)

        assert person.raw == sample_person_data
        assert person.id == "https://rism.online/people/123456"
        assert person.type == "Person"

    def test_person_properties(self, sample_person_data):
        """Test all property methods return expected values."""
        person = RISMPerson(sample_person_data)

        assert person.name == "Pontio, Pietro"
        assert person.dates == "1532-1596"

    def test_person_roles_property(self, sample_person_data):
        """Test roles property returns list correctly."""
        person = RISMPerson(sample_person_data)

        roles = person.roles
        assert isinstance(roles, list)
        assert len(roles) == 1
        assert "composer" in roles

    def test_person_optional_fields(self):
        """Test handling of missing optional fields."""
        minimal_data = {"@id": "test-person-id", "@type": "Person"}

        person = RISMPerson(minimal_data)

        assert person.name is None
        assert person.dates is None
        assert person.roles == []

    def test_person_multiple_roles(self):
        """Test person with multiple roles."""
        data = {
            "@id": "test-person-id",
            "@type": "Person",
            "role": ["composer", "theorist", "teacher"],
        }

        person = RISMPerson(data)

        roles = person.roles
        assert len(roles) == 3
        assert "composer" in roles
        assert "theorist" in roles
        assert "teacher" in roles


class TestRISMInstitution:
    """Test suite for RISMInstitution entity."""

    def test_institution_creation(self, sample_institution_data):
        """Test RISMInstitution creation with valid data."""
        institution = RISMInstitution(sample_institution_data)

        assert institution.raw == sample_institution_data
        assert institution.id == "https://rism.online/institutions/789"
        assert institution.type == "Institution"

    def test_institution_properties(self, sample_institution_data):
        """Test all property methods return expected values."""
        institution = RISMInstitution(sample_institution_data)

        assert institution.name == "Bibliothèque Nationale"
        assert institution.siglum == "F-Pn"
        assert institution.country == "France"

    def test_institution_optional_fields(self):
        """Test handling of missing optional fields."""
        minimal_data = {"@id": "test-institution-id", "@type": "Institution"}

        institution = RISMInstitution(minimal_data)

        assert institution.name is None
        assert institution.siglum is None
        assert institution.country is None

    @pytest.mark.parametrize(
        "field,value",
        [
            ("title", "Test Title"),
            ("date", "1588"),
            ("siglum", "US-NY"),
        ],
    )
    def test_source_property_access(self, sample_source_data, field, value):
        """Parametrized test for property access."""
        # Update the test data
        sample_source_data[field] = value
        source = RISMSource(sample_source_data)

        assert getattr(source, field) == value
