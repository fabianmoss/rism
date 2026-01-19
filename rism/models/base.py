from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class RISMEntry:
    """
    Base class for all RISM domain objects.
    """

    raw: Dict[str, Any]
    id: str = field(init=False)
    type: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "id", self.raw.get("@id"))
        object.__setattr__(self, "type", self.raw.get("@type"))

    def to_dict(self) -> Dict[str, Any]:
        """Return raw JSON-LD data."""
        return self.raw

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"
