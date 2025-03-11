from aiogram import Router, F
from aiogram.types import Message
from dowload_from_youtube import ytd_obj
from keyboards import get_kb__downloadMP3
from messages_text import youtube_metadata_message, commands_text


router = Router()


# @router.message(Text(startswith="https://www.youtu"))  # Хендлер срабатывает на любое текстовое сообщение
@router.message(lambda message: message.text.startswith("https://www.youtu"))  # Используем лямбду для фильтрации
async def get_youtube_metadata(message: Message):

    url = message.text
    metadata = await ytd_obj.get_metadata(url)
    if metadata['status']:
        await message.reply(
            text=youtube_metadata_message(metadata), parse_mode='HTML',
            reply_markup=get_kb__downloadMP3('dwnld', url, message.from_user.id))
    else:
        response = metadata['massage']
        await message.reply(text=response)


@router.message(F.text.startswith("/start"))
async def start_training(message: Message):
    await message.answer(text=commands_text['help'])

@router.message(F.text.startswith("/help"))
async def start_training(message: Message):
    await message.answer(text=commands_text['help'])


