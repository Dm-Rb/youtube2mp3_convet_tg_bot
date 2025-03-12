buttons = \
    {
    'download': "🎧 Download MP3"
    }
messages = {
    'wait': "Ваш запыт апрацоўваецца, чакайце калі-ласка. У залежнасці ад памера файла час адказа бота можа дасягнуць некалькі хвілін"
    }

exceptions = {
    'audio_sent': "Памылка пры адпраўленні файла ў telegram"
}
commands_text = {
    'help': 'Адпраўце боту спасылку на відэа YouTube. Бот cканвертуе відэа ў mp3-файл.',
    'start': 'Адпраўце боту спасылку на відэа YouTube. Бот cканвертуе відэа ў mp3-файл.'
}


def youtube_metadata_message(metadata: dict):
    if metadata['view_count']:
        views = " ".join(str(metadata['view_count'])[::-1][i:i + 3] for i in range(0, len(str(metadata['view_count'])), 3))[::-1]
    else:
        views = 'Няма інфармацыі'
    if metadata['duration']:
        h, m, s = int(metadata['duration']) // 3600, (int(metadata['duration']) % 3600) // 60, int(metadata['duration']) % 60
        duration = f"{h:02}:{m:02}:{s:02}"
    else:
        duration = 'Няма інфармацыі'

    message = (f"⇨ <b>Назва:</b> {metadata['title']}\n"
                f"⇨ <b>Канал:</b> {metadata['uploader']}\n"
                f"⇨ <b>Працягласць відэа:</b> {duration}\n"
                f"⇨ <b>Колькасць праглядаў:</b> {views}\n"
               )
    if metadata['filesize']:
        message += f'⇨ Памер файла відэа: {metadata["view_count"]}\n'
    return message

