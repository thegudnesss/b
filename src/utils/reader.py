from pathlib import Path
import json
from typing import Any

DATA_DIR = Path(__file__).parent.parent / "data"

def read_json(filename: str) -> Any:
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(filename: str, data: Any) -> None:
    path = DATA_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
