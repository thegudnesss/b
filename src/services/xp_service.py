from __future__ import annotations
from typing import Optional
from math import pow

from src.utils.reader import read_json, write_json
from src.database import User, XPLog, mongo
from datetime import datetime

class XPService:
    def __init__(self, base_xp: int = 100, multiplier: float = 1.5) -> None:
        self.base_xp = base_xp
        self.multiplier = multiplier
        self.levels_file = "levels.json"
        self.levels = read_json(self.levels_file)

    def rebuild_levels(self, max_level: int = 20) -> None:
        """Formula asosida levellar.json ni qayta tuzadi."""
        levels_data = []
        for lvl in range(1, max_level + 1):
            xp_needed = int(self.base_xp * pow(lvl, self.multiplier))
            levels_data.append({
                "name": self.level_name(lvl),
                "level": lvl,
                "xp_needed": xp_needed
            })
        write_json(self.levels_file, levels_data)
        self.levels = levels_data

    def level_name(self, level: int) -> str:
        """Daraja nomlarini belgilash (keyin ixtiyoriy o‘zgartirish mumkin)."""
        names = ["E", "D", "C", "B", "A", "S", "SS", "SSS", "Legend", "Myth"]
        return names[level - 1] if 1 <= level <= len(names) else f"Level {level}"

    def get_level_by_xp(self, xp: int) -> dict:
        """XP ga qarab darajani aniqlash."""
        for lvl in reversed(self.levels):
            if xp >= lvl["xp_needed"]:
                return lvl
        return self.levels[0]

    def xp_to_next_level(self, xp: int) -> int:
        """Keyingi darajaga nechta XP kerakligini hisoblaydi."""
        current_level = self.get_level_by_xp(xp)
        idx = current_level["level"]
        if idx >= len(self.levels):
            return 0
        return self.levels[idx]["xp_needed"] - xp

    async def add_xp(self, user_id: int, amount: int, reason: str) -> None:
        """Foydalanuvchiga XP qo‘shish va logga yozish."""
        user = await User.get({"_id": user_id})
        if not user:
            user = User(_id=user_id, xp=0)
            await User.create(user)

        new_xp = user.xp + amount
        await User.update({"_id": user_id}, {"xp": new_xp})

        log = XPLog(
            user_id=user_id,
            change=amount,
            reason=reason,
            date=datetime.utcnow()
        )
        await XPLog.create(log)

    async def remove_xp(self, user_id: int, amount: int, reason: str) -> None:
        """Foydalanuvchidan XP ayirish."""
        await self.add_xp(user_id, -abs(amount), reason)

    async def set_xp(self, user_id: int, new_xp: int, reason: str) -> None:
        """Foydalanuvchi XP sini bevosita o‘rnatish."""
        await User.update({"_id": user_id}, {"xp": new_xp})
        log = XPLog(
            user_id=user_id,
            change=f"Set to {new_xp}",
            reason=reason,
            date=datetime.utcnow()
        )
        await XPLog.create(log)

    async def get_user_level_info(self, user_id: int) -> Optional[dict]:
        """Foydalanuvchining XP va daraja ma’lumotlari."""
        user = await User.get({"_id": user_id})
        if not user:
            return None
        level_info = self.get_level_by_xp(user.xp)
        return {
            "user_id": user_id,
            "xp": user.xp,
            "level": level_info["name"],
            "xp_to_next": self.xp_to_next_level(user.xp)
        }

# Global servis
xp_service = XPService()
