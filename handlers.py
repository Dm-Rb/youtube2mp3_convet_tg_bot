from aiogram import Router, F
from aiogram.types import Message
from dowload_from_youtube import ytd_obj
from keyboards import get_kb__downloadMP3
from messages_text import youtube_metadata_message, commands_text
###4
from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from dowload_from_youtube import ytd_obj
from aiogram.types import FSInputFile
from pathlib import Path
from messages_text import messages, exceptions
import os

router = Router()


# @router.message(Text(startswith="https://www.youtu"))  # Хендлер срабатывает на любое текстовое сообщение
@router.message(lambda message: message.text.startswith("https://www.youtu") or message.text.startswith("https://youtu"))  # Используем лямбду для фильтрации
async def get_youtube_metadata(message: Message):

    url = message.text
    metadata = await ytd_obj.get_metadata(url)
    video_id = metadata.get('video_id', '')
    if metadata['status']:
        await message.reply(
            text=youtube_metadata_message(metadata),
            parse_mode='HTML',
            disable_web_page_preview=True,
            reply_markup=get_kb__downloadMP3('dwnld', video_id, message.from_user.id))
    else:
        response = metadata['massage']
        await message.reply(text=response)


@router.message(F.text.startswith("/start"))
async def start_training(message: Message):
    await message.answer(text=commands_text['help'])

@router.message(F.text.startswith("/help"))
async def send_audio_handler(message: Message, bot: Bot):  # Добавляем bot в параметры
    input_file = FSInputFile(path=os.path.join('downloads', 'AFX (Aphex Twin) - 28 organ.mp3'))
    await bot.send_audio(chat_id=message.chat.id, audio=input_file)


