from __future__ import annotations

import argparse
from pathlib import Path

from config_store import write_config
from engine import TorchEngine


def _ask(prompt: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or (default or "")


def cmd_init(config_path: Path, show_tokens: bool) -> None:
    project_name = _ask("Project name")
    goal = _ask("Project goal")
    num_agents = int(_ask("Number of agents", "3"))

    agents = []
    for idx in range(1, num_agents + 1):
        role = _ask(f"Role for Agent {idx} (feature/test/refactor)", "feature")
        agents.append({"name": f"Agent {idx}", "role": role})

    workflow_raw = _ask("Workflow order (comma-separated roles)", "feature,test,refactor")
    workflow = [x.strip() for x in workflow_raw.split(",") if x.strip()]
    token_budget = int(_ask("Token budget", "5000"))

    config = {
        "project_name": project_name,
        "goal": goal,
        "agents": agents,
        "workflow": workflow,
        "token_budget": token_budget,
    }

    written = write_config(config, config_path)
    print(f"Wrote config to {written}")

    if show_tokens:
        tracker = TorchEngine(config).token_tracker
        print(tracker.render_ascii_bar())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="torch", description="Torch v0 CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a project_config.json")
    init_parser.add_argument("--config", type=Path, default=Path("project_config.json"))
    init_parser.add_argument("--show-tokens", action="store_true")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        cmd_init(config_path=args.config, show_tokens=args.show_tokens)


if __name__ == "__main__":
    main()
