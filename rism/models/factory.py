from .base import RISMEntry
from .entities import RISMSource, RISMPerson, RISMInstitution
from typing import Any, Dict
from .collections import (
    RISMEntryCollection,
    RISMSourceCollection,
    RISMPersonCollection,
    RISMInstitutionCollection,
)


def parse_rism_entry(raw: Dict[str, Any]) -> RISMEntry:
    entry_type = raw.get("@type")

    if entry_type == "Source":
        return RISMSource(raw)
    if entry_type == "Person":
        return RISMPerson(raw)
    if entry_type == "Institution":
        return RISMInstitution(raw)

    return RISMEntry(raw)


def parse_rism_collection(
    raw_items: list[dict], *, raise_if_empty=False
) -> RISMEntryCollection:
    if not raw_items:
        if raise_if_empty:
            raise ValueError("Empty collection")
        return RISMEntryCollection([])  # empty collection

    entries = [parse_rism_entry(raw) for raw in raw_items]

    # type-based collection
    entry_type = type(entries[0])
    if entry_type is RISMSource:
        return RISMSourceCollection(entries)
    if entry_type is RISMPerson:
        return RISMPersonCollection(entries)
    if entry_type is RISMInstitution:
        return RISMInstitutionCollection(entries)

    return RISMEntryCollection(entries)
