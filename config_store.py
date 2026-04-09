from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


DEFAULT_CONFIG_PATH = Path("project_config.json")


def write_config(config: Dict[str, Any], path: Path = DEFAULT_CONFIG_PATH) -> Path:
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return path


def read_config(path: Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
