from __future__ import annotations

import argparse
import getpass
from pathlib import Path

from config_store import write_config
from engine import TorchEngine
from openai import OpenAI


OPENAI_MODELS = [
    "gpt-4.1-mini",
    "gpt-4.1",
    "gpt-4o-mini",
]


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


def _choose_model() -> str:
    print("Available OpenAI models:")
    for idx, model in enumerate(OPENAI_MODELS, start=1):
        print(f"  {idx}. {model}")

    while True:
        raw_choice = _ask("Pick a model by number", "1")
        try:
            selected_idx = int(raw_choice)
            if 1 <= selected_idx <= len(OPENAI_MODELS):
                return OPENAI_MODELS[selected_idx - 1]
        except ValueError:
            pass
        print("Invalid selection. Please enter one of the listed numbers.")


def cmd_chat() -> None:
    model = _choose_model()
    api_key = getpass.getpass("Enter your OpenAI API key: ").strip()
    if not api_key:
        raise ValueError("API key is required to run chat.")

    client = OpenAI(api_key=api_key)
    messages: list[dict[str, str]] = []

    seed_prompt = _ask("Optional starting prompt (leave blank to skip)", "")
    if seed_prompt:
        messages.append({"role": "user", "content": seed_prompt})

    print("Chat started. Type 'exit' or 'quit' to stop.")
    while True:
        prompt = input("You: ").strip()
        if prompt.lower() in {"exit", "quit"}:
            print("Bye.")
            return
        if not prompt:
            continue

        messages.append({"role": "user", "content": prompt})
        response = client.responses.create(model=model, input=messages)
        reply_text = response.output_text
        print(f"{model}: {reply_text}")
        messages.append({"role": "assistant", "content": reply_text})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="torch", description="Torch v0 CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a project_config.json")
    init_parser.add_argument("--config", type=Path, default=Path("project_config.json"))
    init_parser.add_argument("--show-tokens", action="store_true")
    subparsers.add_parser("chat", help="Start a terminal chat with an OpenAI model")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        cmd_init(config_path=args.config, show_tokens=args.show_tokens)
    elif args.command == "chat":
        cmd_chat()


if __name__ == "__main__":
    main()
