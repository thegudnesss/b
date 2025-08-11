# src/utils/xp_manager.py
from __future__ import annotations
from typing import Any
import json
from pathlib import Path
import math

BASE_DIR = Path(__file__).resolve().parent.parent.parent / "data"


class XPManager:
    _levels_file = BASE_DIR / "levels.json"
    _xp_config_file = BASE_DIR / "xp_config.json"

    def __init__(self) -> None:
        self._levels: list[str] = self._read_json(self._levels_file)
        self._config: dict[str, Any] = self._read_json(self._xp_config_file)

    @staticmethod
    def _read_json(file_path: Path) -> Any:
        if not file_path.exists():
            raise FileNotFoundError(f"❌ {file_path.name} topilmadi!")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _write_json(file_path: Path, data: Any) -> None:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def update_config(self, base_xp: int, multiplier: float) -> dict:
        """Darajalar bo‘yicha XP ni yangilash va saqlash."""
        xp_table = {
            level: round(base_xp * (index ** multiplier))
            for index, level in enumerate(self._levels, start=1)
        }
        self._config = {
            "base_xp": base_xp,
            "multiplier": multiplier,
            "xp_table": xp_table
        }
        self._write_json(self._xp_config_file, self._config)
        return self._config

    def get_xp_for_level(self, level_name: str) -> int:
        """Berilgan daraja uchun XP miqdorini olish."""
        return self._config["xp_table"].get(level_name, 0)

    def get_level_for_xp(self, xp: int) -> str:
        """XP asosida daraja nomini aniqlash."""
        xp_table = self._config["xp_table"]
        for level, needed_xp in reversed(xp_table.items()):
            if xp >= needed_xp:
                return level
        return self._levels[0]

    def get_all_levels(self) -> dict:
        """Darajalar va ularning XP larini olish."""
        return self._config["xp_table"]


# Global obyekt (istalgan joyda chaqirish mumkin)
xp_manager = XPManager()
