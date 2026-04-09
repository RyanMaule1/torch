from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class TokenTracker:
    """Tracks token usage at the project and per-agent level."""

    budget: int
    by_agent: Dict[str, int] = field(default_factory=dict)

    def record(self, agent_name: str, used: int) -> None:
        self.by_agent[agent_name] = self.by_agent.get(agent_name, 0) + used

    @property
    def used_total(self) -> int:
        return sum(self.by_agent.values())

    @property
    def remaining(self) -> int:
        return self.budget - self.used_total

    def render_ascii_bar(self, width: int = 30) -> str:
        """Returns a simple ASCII progress bar based on token budget."""

        if self.budget <= 0:
            return "[no budget set]"

        ratio = min(max(self.used_total / self.budget, 0), 1)
        filled = int(width * ratio)
        bar = "#" * filled + "-" * (width - filled)
        return f"[{bar}] {self.used_total}/{self.budget} tokens"
