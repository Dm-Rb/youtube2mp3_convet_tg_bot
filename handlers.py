from aiogram import F
from aiogram.types import Message
from keyboards import get_kb__downloadMP3
from messages_text import youtube_metadata_message, commands_text
from aiogram import Router, Bot
from dowload_from_youtube import ytd_obj


router = Router()


@router.message(lambda message: "youtu" in message.text)  # Используем лямбду для фильтрации
async def get_youtube_metadata(message: Message):

    url = message.text
    metadata: dict = await ytd_obj.get_metadata(url)
    if metadata['status']:
        video_id = metadata.get('video_id', '')
        await message.reply(
            text=youtube_metadata_message(metadata),
            parse_mode='HTML',
            disable_web_page_preview=True,
            reply_markup=get_kb__downloadMP3('dwnld', video_id, message.from_user.id))
    else:
        response = metadata['message']
        await message.reply(text=response, parse_mode='HTML')


@router.message(F.text.startswith("/start"))
async def start_training(message: Message):
    await message.answer(text=commands_text['start'])


@router.message(F.text.startswith("/help"))
async def send_audio_handler(message: Message, bot: Bot):  # Добавляем bot в параметры
    await message.answer(text=commands_text['help'])


