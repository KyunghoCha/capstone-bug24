from pathlib import Path
from ai.config import load_config

ROOT = Path(__file__).resolve().parents[2]   # .../safety-cctv-ai
cfg_path = ROOT / "configs" / "default.yaml"

cfg = load_config(cfg_path)

print(cfg.get("source", {}))
