# src/utils/reader.py
from __future__ import annotations
from typing import Any, Optional
import json
from pathlib import Path


class JSONReader:
    def __init__(self, base_dir: Optional[Path] = None) -> None:
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent.parent / "locales"
        self._cache: dict[str, Any] = {}

    def _get_path(self, file_name: str) -> Path:
        if not file_name.endswith(".json"):
            file_name += ".json"
        return self.base_dir / file_name

    def _load_from_disk(self, path: Path) -> Any:
        if not path.exists():
            raise FileNotFoundError(f"❌ Fayl topilmadi: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def read(self, file_name: str) -> Any:
        """JSON faylni o‘qish (cache bilan)."""
        path = str(self._get_path(file_name))
        if path not in self._cache:
            self._cache[path] = self._load_from_disk(Path(path))
        return self._cache[path]

    def write(self, file_name: str, data: Any) -> None:
        """JSON faylga yozish va cache yangilash."""
        path = self._get_path(file_name)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self._cache[str(path)] = data

    def get_nested(self, file_name: str, key_path: str, default: Any = None) -> Any:
        """Ichma-ich qiymat olish (menu.main.start_button)."""
        data = self.read(file_name)
        for key in key_path.split("."):
            if isinstance(data, dict):
                data = data.get(key, default)
            else:
                return default
        return data

    def update(self, file_name: str, key_path: str, value: Any) -> None:
        """Ichma-ich qiymatni yangilash (a.b.c = value)."""
        data = self.read(file_name)
        keys = key_path.split(".")
        temp = data
        for key in keys[:-1]:
            if key not in temp or not isinstance(temp[key], dict):
                temp[key] = {}
            temp = temp[key]
        temp[keys[-1]] = value
        self.write(file_name, data)


# Global obyekt
reader = JSONReader()
