"""
BozorBot package
================
Bu modul bot va dispatcher obyektlarini global holatda yaratadi,
shuningdek `config` orqali sozlamalarni ulaydi.
"""

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config.settings import config
from src.utils.logging import log

# Bot obyektini yaratamiz
bot: Bot = Bot(
    token=config.bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

log.info("Starting bot...")

# Dispatcher obyektini yaratamiz
dp: Dispatcher = Dispatcher()

__all__ = ["bot", "dp", "config", "log"]