from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import Message
from src.database import user_repo, User  # __init__.py dan keladi


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user = await user_repo.get({"_id": event.from_user.id})
        if not user:
            user = User(_id=event.from_user.id)
            await user_repo.create(user)
        data["user"] = user
        return await handler(event, data)
