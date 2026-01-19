from .entities import RISMInstitution, RISMPerson, RISMSource
from dataclasses import dataclass, field
from typing import Generic, List, Type, TypeVar

from .base import RISMEntry

T = TypeVar("T", bound=RISMEntry)


@dataclass
class RISMEntryCollection(Generic[T]):
    """
    Base collection for homogeneous RISMEntry types.
    """

    entries: List[T]
    entry_type: Type[T] = field(init=False)

    def __post_init__(self):
        if not self.entries:
            raise ValueError("RISMEntryCollection cannot be empty")

        first_type = type(self.entries[0])

        for e in self.entries:
            if not isinstance(e, first_type):
                raise TypeError(
                    f"All entries must be of the same type. "
                    f"Expected {first_type.__name__}, got {type(e).__name__}"
                )

        self.entry_type = first_type

    def __iter__(self):
        return iter(self.entries)

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, idx):
        return self.entries[idx]

    def ids(self) -> List[str]:
        return [e.id for e in self.entries]

    def to_dicts(self) -> List[dict]:
        return [e.to_dict() for e in self.entries]


class RISMSourceCollection(RISMEntryCollection[RISMSource]):
    pass


class RISMPersonCollection(RISMEntryCollection[RISMPerson]):
    pass


class RISMInstitutionCollection(RISMEntryCollection[RISMInstitution]):
    pass
