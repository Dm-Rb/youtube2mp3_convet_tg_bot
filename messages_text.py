inline_buttons = \
    {
    'download': "Download MP3"
    }


def youtube_metadata_message(metadata: dict):
    message = (f"Название: {metadata['title']}\n"
                f"Автор: {metadata['uploader']}\n"
                f"Длительность: {metadata['duration']} сек.\n"
                f"Просмотры: {metadata['view_count']}\n"
                f"Размер файла: {metadata['filesize']}")
    return message