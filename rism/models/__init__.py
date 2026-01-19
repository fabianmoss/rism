"""
Domain models for RISM entities and collections.
"""

from .base import RISMEntry

from .entities import (
    RISMSource,
    RISMPerson,
    RISMInstitution,
)

from .collections import (
    RISMEntryCollection,
    RISMSourceCollection,
    RISMPersonCollection,
    RISMInstitutionCollection,
)

from .factory import (
    parse_rism_entry,
    parse_rism_collection,
)

__all__ = [
    # Base
    "RISMEntry",
    # Entities
    "RISMSource",
    "RISMPerson",
    "RISMInstitution",
    # Collections
    "RISMEntryCollection",
    "RISMSourceCollection",
    "RISMPersonCollection",
    "RISMInstitutionCollection",
    # Factories
    "parse_rism_entry",
    "parse_rism_collection",
]
