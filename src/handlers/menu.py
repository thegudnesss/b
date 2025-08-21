from aiogram import Router
from aiogram.types import CallbackQuery
from src.utils.callbacks import MenuCallback
from src.services.page_service import menu_service

router = Router()


@router.callback_query(MenuCallback.filter())
async def menu_handler(query: CallbackQuery, callback_data: MenuCallback):
    await menu_service.render(query, callback_data.path)
