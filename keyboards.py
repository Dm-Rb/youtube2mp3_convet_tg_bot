from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from messages_text import buttons


def get_kb__downloadMP3(fuc_type: str, url: str, user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=buttons['download_128'],
                    callback_data=f"{fuc_type};{url};{str(user_id)};128"
                )
            ],
            [
                InlineKeyboardButton(
                    text=buttons['download_192'],
                    callback_data=f"{fuc_type};{url};{str(user_id)};192"
                )
            ],
            [
                InlineKeyboardButton(
                    text=buttons['download_256'],
                    callback_data=f"{fuc_type};{url};{str(user_id)};256"
                )
            ],
            [
                InlineKeyboardButton(
                    text=buttons['download_320'],
                    callback_data=f"{fuc_type};{url};{str(user_id)};320"
                )
            ]
        ]
    )
