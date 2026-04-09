from __future__ import annotations

from abc import ABC, abstractmethod

from state import ChangeSet, ProjectState


class Agent(ABC):
    """Base interface for all Torch agents."""

    def __init__(self, name: str, role: str) -> None:
        self.name = name
        self.role = role

    @abstractmethod
    def run(self, state: ProjectState) -> ChangeSet:
        """Run this agent over the current state and return a ChangeSet."""
