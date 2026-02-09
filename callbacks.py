from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from dowload_from_youtube import ytd_obj
from aiogram.types import FSInputFile
from messages_text import messages
from users_history import data_base_obj
import os


router = Router()


async def send_file(chat_id, file_path, bot: Bot) -> str:
    sent_message = await bot.send_audio(
        chat_id=chat_id,
        audio=FSInputFile(file_path)
    )
    return sent_message.audio.file_id


@router.callback_query(lambda callback: callback.data.startswith("dwnld;"))
async def process_download_send(callback: CallbackQuery, bot: Bot):
    action, video_id, user_id, bitrate = callback.data.split(";")
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer(messages['wait'], show_alert=True)

    path2file = None
    try:
        response = await ytd_obj.download_video_extract_audio(f'https://www.youtube.com/watch?v={video_id}', bitrate)
        
        if not response['status']:
            await bot.send_message(chat_id=callback.message.chat.id, text=response['massage'])
            return
        path2file = response['message']

        user = callback.from_user.first_name
        file_id = await send_file(callback.message.chat.id, path2file, bot)

        await data_base_obj.add_new_row(
            tg_user_id=callback.from_user.id,  # Используйте ID пользователя, а не чата
            tg_user_full_name=user,
            file_title=os.path.splitext(os.path.basename(path2file))[0],
            tg_file_id=file_id,
            mp3_bitrate=int(bitrate)
        )
    except Exception as e:
        print(e)
    finally:
        # del files frm disc
        if path2file:
            dir_path = os.path.dirname(path2file)
            base_name = os.path.splitext(os.path.basename(path2file))[0]

            for filename in os.listdir(dir_path):
                if filename.startswith(base_name):
                    full_path = os.path.join(dir_path, filename)
                    if os.path.isfile(full_path):
                        os.remove(full_path)

