from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from messages_text import buttons


def get_kb__downloadMP3(fuc_type: str, url: str, user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=buttons['download'],
                    callback_data=f"{fuc_type};{url};{str(user_id)}"
                )
            ]
        ]
    )
