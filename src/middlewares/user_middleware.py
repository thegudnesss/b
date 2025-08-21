from typing import Any, Awaitable, Callable, Dict, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, InlineQuery

from src.database import User, user_repo
from src.services.xp_service import xp_service


TelegramEvent = Union[Message, CallbackQuery, InlineQuery]


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramEvent, Dict[str, Any]], Awaitable[Any]],
        event: TelegramEvent,
        data: Dict[str, Any]
    ) -> Any:
        # user_id olish
        user_id = event.from_user.id

        # Bazadan olish yoki yaratish
        user = await user_repo.get({"_id": user_id})
        if not user:
            user = User(_id=user_id)
            await user_repo.create(user)

        # XP boyitish
        enriched_user = xp_service.enrich_user_data(user)

        # Eventga joylash
        event.user = enriched_user  # type: ignore

        return await handler(event, data)
