from aiogram import Router, Bot
from aiogram.types import CallbackQuery, InputFile
from dowload_from_youtube import ytd_obj
from aiogram.types import FSInputFile
from pathlib import Path

router = Router()


@router.callback_query(lambda callback: callback.data.startswith("dwnld;"))
async def process_word_response(callback: CallbackQuery, bot: Bot):
    # Извлекаем данные из callback_data
    action, url, user_id = callback.data.split(";")
    print(action, url, user_id)

    # Отвечаем на callback-запрос сразу
    await callback.answer("Обработка запроса...")

    if url.startswith("https://www.youtu"):
        try:
            # Обработка, логика
            path2file = await ytd_obj.download_video_extract_audio(url)

            # Создаем объект FSInputFile
            input_file = FSInputFile(path=path2file, filename=Path(path2file).name)

            # Отправляем аудио
            await bot.send_audio(chat_id=callback.message.chat.id, audio=input_file)
            await callback.message.edit_reply_markup(reply_markup=None)

            # Уведомляем пользователя об успешной отправке
            # await bot.send_message(chat_id=callback.message.chat.id, text="Аудио успешно отправлено!")

        except Exception as e:
            # Если произошла ошибка, отправляем сообщение об ошибке
            await bot.send_message(chat_id=callback.message.chat.id, text=f"Ошибка при отправке аудио: {e}")

    # "yes:{word}:{str(word_id)}:{str(user_id)}:{fuc_type}"
    # if action == "yes":
    #     if fuc_type == 'add':
    #         await database.add_row__user_data(user_id, int(word_id))
    #         await callback.answer(f"{word.capitalize()}\n добавлено в словарь изучения!", show_alert=False)
    #     elif fuc_type == 'del':
    #         await database.del_row__user_data(user_id, int(word_id))
    #         await callback.answer(f"{word.capitalize()}\n удалено из словаря изучения!", show_alert=False)
    #
    # # Удаляем сообщение вместе с клавиатурой
    # await callback.message.delete()
    # # Уведомляем Telegram, что callback обработан
    # await callback.answer()