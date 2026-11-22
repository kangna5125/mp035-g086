"""Load params.yaml and resolve paths relative to the repository root."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_params(path=None):
    """Read params.yaml (default: repo root) and return it as a dict."""
    path = Path(path) if path else ROOT / "params.yaml"
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
