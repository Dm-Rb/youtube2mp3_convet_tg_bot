from aiogram import Router, F
from aiogram.types import Message
from dowload_from_youtube import ytd_obj
from keyboards import get_kb__downloadMP3
from messages_text import youtube_metadata_message


router = Router()


# @router.message(Text(startswith="https://www.youtu"))  # Хендлер срабатывает на любое текстовое сообщение
@router.message(lambda message: message.text.startswith("https://www.youtu"))  # Используем лямбду для фильтрации
async def get_youtube_metadata(message: Message):

    url = message.text
    metadata = await ytd_obj.get_metadata(url)
    print(metadata)
    if metadata['status']:
        await message.reply(
            text=youtube_metadata_message(metadata),
            reply_markup=get_kb__downloadMP3('dwnld', url, message.from_user.id))
    else:
        response = metadata['massage']
        await message.reply(text=response)
