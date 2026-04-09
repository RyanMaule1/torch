from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ChangeSet:
    """Represents files produced by an agent during one workflow step."""

    files: Dict[str, str]
    agent_name: str
    token_used: int


@dataclass
class ProjectState:
    """Mutable state shared across sequential agent runs."""

    goal: str
    files: Dict[str, str] = field(default_factory=dict)
    changesets: List[ChangeSet] = field(default_factory=list)

    def apply_changeset(self, changeset: ChangeSet) -> None:
        """Apply file updates and retain change history."""

        self.files.update(changeset.files)
        self.changesets.append(changeset)
