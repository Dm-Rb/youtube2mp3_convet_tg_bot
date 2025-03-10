from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from messages_text import inline_buttons


def get_kb__downloadMP3(fuc_type: str, url: str, file_name: str, user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=inline_buttons['download'],
                    callback_data=f"{fuc_type}:{url}:{file_name}:{str(user_id)}"
                )
            ]
        ]
    )
