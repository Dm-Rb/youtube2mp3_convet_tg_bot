from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from dowload_from_youtube import ytd_obj
from aiogram.types import FSInputFile
# from pathlib import Path
from messages_text import messages, exceptions
import os
from users_history import data_base_obj

router = Router()


@router.callback_query(lambda callback: callback.data.startswith("dwnld;"))
async def process_word_response(callback: CallbackQuery, bot: Bot):
    # Извлекаем данные из callback_data
    action, video_id, user_id, bitrate = callback.data.split(";")
    # Отвечаем на callback-запрос сразу
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.answer(messages['wait'], show_alert=True)

    try:
        # Ждём ответ от обработчика
        response = await ytd_obj.download_video_extract_audio(f'https://www.youtube.com/watch?v={video_id}', bitrate)
        # Если статус ответа False - сворачиваем движ
        if not response['status']:
            await bot.send_message(chat_id=callback.message.chat.id, text=response['massage'])
            return

        path2file = response['massage']
        filename = os.path.basename(path2file)
        # Создаем объект FSInputFile
        input_file = FSInputFile(path=path2file, filename=filename)

        # Отправляем аудио
        sent_message = await bot.send_audio(chat_id=callback.message.chat.id, audio=input_file)
        # Аргументы для записи в БД
        audio_file_name = sent_message.audio.file_name
        audio_file_id = sent_message.audio.file_id
        # Записываем в данные в sqlite
        await data_base_obj.add_new_row(
            tg_user_id=callback.message.chat.id,
            file_title=audio_file_name.rstrip('.mp3'),
            url=f'https://www.youtube.com/watch?v={video_id}',
            tg_file_id=audio_file_id,
            mp3_bitrate=bitrate
        )

        if os.path.exists(path2file):
            # Удаляем файл
            os.remove(path2file)

    except Exception as e:
        # Если произошла ошибка, отправляем сообщение об ошибке
        await bot.send_message(chat_id=callback.message.chat.id, text=f"{exceptions['audio_sent']}: {e}")
