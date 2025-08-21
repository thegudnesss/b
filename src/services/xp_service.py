from __future__ import annotations
from typing import Optional
from math import pow

from src.utils.reader import reader
from src.database.models import User, UserRuntime


class XPService:
    def __init__(self, base_xp: int = 100, multiplier: float = 1.5) -> None:
        self.base_xp = base_xp
        self.multiplier = multiplier
        self.levels_file = "levels.json"
        self.levels = reader.read(self.levels_file)

    def rebuild_levels(self, base_xp: Optional[int] = None, multiplier: Optional[float] = None, max_level: int = 20) -> None:
        """Levellarni qayta qurish"""
        if base_xp is not None:
            self.base_xp = base_xp
        if multiplier is not None:
            self.multiplier = multiplier

        levels_data = []
        for lvl in range(1, max_level + 1):
            xp_needed = int(self.base_xp * pow(lvl, self.multiplier))
            levels_data.append({
                "name": self.level_name(lvl),
                "level": lvl,
                "xp_needed": xp_needed
            })
        reader.write(self.levels_file, levels_data)
        self.levels = levels_data

    def level_name(self, level: int) -> str:
        names = ["E", "D", "C", "B", "A", "S", "SS", "SSS", "Legend", "Myth"]
        return names[level - 1] if 1 <= level <= len(names) else f"Level {level}"

    def get_level_by_xp(self, xp: int) -> dict:
        for lvl in reversed(self.levels):
            if xp >= lvl["xp_needed"]:
                return lvl
        return self.levels[0]

    def xp_to_next_level(self, xp: int) -> int:
        current_level = self.get_level_by_xp(xp)
        idx = current_level["level"]
        if idx >= len(self.levels):
            return 0
        return self.levels[idx]["xp_needed"] - xp

    def enrich_user_data(self, user: User) -> UserRuntime:
        """Foydalanuvchini daraja va XP ma’lumotlari bilan boyitish"""
        level_info = self.get_level_by_xp(user.xp)
        idx = level_info["level"]
        xp_needed = level_info["xp_needed"]
        xp_to_next = self.xp_to_next_level(user.xp)

        progress_percent = round(
            ((user.xp - xp_needed + xp_to_next) / (xp_needed if xp_needed else 1)) * 100, 2
        )

        return UserRuntime(
            **user.dict(),
            level_name=level_info["name"],
            level_num=idx,
            next_level=self.level_name(idx + 1) if idx < len(self.levels) else None,
            xp_to_next=xp_to_next,
            total_xp_needed=xp_needed,
            progress_percent=progress_percent
        )


xp_service = XPService()
