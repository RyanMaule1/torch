# torch

Torch is a CLI-based project initializer and workflow generator for multi-agent development loops.

## v0 Scope

- Generate JSON configs for project goals, agent roles, workflow order, and token budgets.
- Provide a CLI (`torch init`) for project setup/configuration.
- Support basic GitHub integration hooks for branch creation, commits, and PR creation.
- Track token usage per agent with optional ASCII visualization.
- Start a direct terminal chat loop with selectable OpenAI models.

## Project Structure

```text
.
├── cli.py
├── engine.py
├── agents/
│   ├── __init__.py
│   ├── base.py
│   ├── feature_agent.py
│   ├── test_agent.py
│   └── refactor_agent.py
├── github_integration.py
├── config_store.py
├── token_tracker.py
├── state.py
├── requirements.txt
└── README.md
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python cli.py init
python cli.py chat
```

## CLI: `torch init`

The init command prompts for:
- Project name
- Project goal
- Number of agents
- Agent roles
- Workflow order (comma-separated roles)
- Token budget

It writes `project_config.json` by default.

## CLI: `torch chat`

The chat command:
- Lists a small starter set of OpenAI models.
- Prompts for your model selection.
- Prompts for your OpenAI API key.
- Optionally accepts a seed prompt before the interactive loop starts.
- Lets you paste prompts directly into the terminal and prints model responses.

## Example Config

```json
{
  "project_name": "StageSphere",
  "goal": "Build a multi-agent project builder",
  "agents": [
    {"name": "Agent 1", "role": "feature"},
    {"name": "Agent 2", "role": "test"},
    {"name": "Agent 3", "role": "refactor"}
  ],
  "workflow": ["feature", "test", "refactor"],
  "token_budget": 5000
}
```
