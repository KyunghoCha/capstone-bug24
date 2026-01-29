# src/ai/config.py
from __future__ import annotations

from pathlib import Path
import yaml

def load_config(config_path: str | Path) -> dict:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path.resolve()}")

    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {path}") from e

    if not isinstance(data, dict):
        raise ValueError(f"Top-level YAML must be a mapping(dict): {path}")

    return data
