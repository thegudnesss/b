from aiogram.types import Message, CallbackQuery

from src.utils.reader import JSONReader

from src.utils.keyboard import inline_builder

from src.utils.callbacks import MenuCallback

class MenuService:
    def __init__(self, file_name: str = "menus") -> None:
        self.file_name = file_name

    def get_page(self, path: str) -> dict | None:
        return JSONReader.get_nested(self.file_name, path)

    def build_markup(self, page: dict):
        buttons = page.get("buttons", [])
        return inline_builder(
            text=[btn["text"] for row in buttons for btn in row],
            callback_data=[btn["callback"] for row in buttons for btn in row],
            sizes=[len(row) for row in buttons],
            class_name=MenuCallback
        )

    async def render(self, message: Message | CallbackQuery, path: str):
        is_callback = isinstance(message, CallbackQuery)
        message = message.message if is_callback else message
        page = self.get_page(path)
        if not page:
            if isinstance(message, CallbackQuery):
                await message.answer("❌ Sahifa topilmadi", show_alert=True)
            else:
                await message.answer("❌ Sahifa topilmadi")
            return

        text = page.get("text", "...")
        markup = self.build_markup(page)

        if isinstance(message, CallbackQuery):
            await message.message.edit_text(text, reply_markup=markup)
        else:
            await message.answer(text, reply_markup=markup)


menu_service = MenuService()

git add.

git commit -m "Refactor MenuService and update menu handler"

git push origin main