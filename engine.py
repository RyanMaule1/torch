from __future__ import annotations

from dataclasses import dataclass

from agents import FeatureAgent, RefactorAgent, TestAgent
from agents.base import Agent
from state import ProjectState
from token_tracker import TokenTracker


AGENT_BY_ROLE = {
    "feature": FeatureAgent,
    "test": TestAgent,
    "refactor": RefactorAgent,
}


@dataclass
class TorchEngine:
    config: dict

    def __post_init__(self) -> None:
        self.state = ProjectState(goal=self.config["goal"])
        self.token_tracker = TokenTracker(budget=self.config["token_budget"])

    def _build_agent(self, role: str, name: str) -> Agent:
        agent_cls = AGENT_BY_ROLE.get(role)
        if not agent_cls:
            raise ValueError(f"Unsupported role in v0: {role}")
        return agent_cls(name=name, role=role)

    def run(self) -> ProjectState:
        role_to_name = {entry["role"]: entry["name"] for entry in self.config["agents"]}

        for role in self.config["workflow"]:
            agent = self._build_agent(role=role, name=role_to_name.get(role, role.title()))
            changeset = agent.run(self.state)
            self.state.apply_changeset(changeset)
            self.token_tracker.record(changeset.agent_name, changeset.token_used)

        return self.state
