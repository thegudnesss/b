from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


def inline_builder(
        text: str | list[str],
        callback_data: str | list[str | dict],  # dict ham bo'lishi mumkin
        sizes: int | list[int] = 2,
        class_name: type[CallbackData] | None = None,
        **kwargs
):
    builder = InlineKeyboardBuilder()

    if isinstance(text, str):
        text = [text]
    if isinstance(callback_data, (str, dict)):
        callback_data = [callback_data]
    if isinstance(sizes, int):
        sizes = [sizes]

    for txt, cb in zip(text, callback_data):
        if class_name:
            if isinstance(cb, dict):
                # dict → fieldlarni avtomatik joylashtiramiz
                callback = class_name(**cb).pack()
            else:
                # oddiy string bo‘lsa → faqat "path"
                callback = class_name(path=cb).pack()
        else:
            callback = cb

        builder.button(text=txt, callback_data=callback)

    builder.adjust(*sizes)
    return builder.as_markup(**kwargs)
