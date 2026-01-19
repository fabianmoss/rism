from typing import List, Optional, Dict
from dataclasses import dataclass
from .base import RISMEntry


@dataclass(frozen=True)
class RISMSource(RISMEntry):
    @property
    def title(self) -> Optional[str]:
        return self.raw.get("title")

    @property
    def date(self) -> Optional[str]:
        return self.raw.get("date")

    @property
    def composers(self) -> List[Dict]:
        return self.raw.get("composer", [])

    @property
    def siglum(self) -> Optional[str]:
        return self.raw.get("siglum")


@dataclass(frozen=True)
class RISMPerson(RISMEntry):
    @property
    def name(self) -> Optional[str]:
        return self.raw.get("name")

    @property
    def dates(self) -> Optional[str]:
        return self.raw.get("date")

    @property
    def roles(self) -> List[str]:
        return self.raw.get("role", [])


@dataclass(frozen=True)
class RISMInstitution(RISMEntry):
    @property
    def siglum(self) -> Optional[str]:
        return self.raw.get("siglum")

    @property
    def name(self) -> Optional[str]:
        return self.raw.get("name")

    @property
    def country(self) -> Optional[str]:
        return self.raw.get("country")
