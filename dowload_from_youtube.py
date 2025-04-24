import yt_dlp
import asyncio
import os
from pathlib import Path
import re

class YouTubeDownloader:

    validate_val = 'youtu'
    output_dir = os.path.join('.', 'downloads')

    def __init__(self):
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

    async def get_metadata(self, url):
        """Асинхронно получает метаданные видео."""
        if self.validate_val not in url:
            return {'status': False, 'massage': 'Bad url'}
        # используем video id, кторый содержится в url.
        # для корректной работы разных url (мобильная версия, короткая ссылка)

        patterns = [
            r'(?:[?&]v=)([^&]+)',  # для ссылок типа youtube.com/watch?v=ID
            r'https?://youtu\.be/([^?]+)'  # для сокращённых ссылок youtu.be/ID
        ]
        video_id = None
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                break

        if video_id:
            url = f"https://www.youtube.com/watch?v={video_id}"
        else:
            return
        yt_dlp_options = {"quiet": True, "noplaylist": True}
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(yt_dlp_options) as ydl:
            info = await loop.run_in_executor(None, ydl.extract_info, url, False)
        return {
            'status': True,
            'massage': "ok",
            'video_id': info.get("id"),
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "duration": info.get("duration"),
            "view_count": info.get('view_count'),
            "filesize": info.get("filesize"),
            "format": info.get("ext"),
            "resolution": info.get("resolution"),
            "direct_url": info.get("url"),
            "thumbnail": info.get('thumbnail')
        }

    async def download_video_extract_audio(self, url, bitrate):
        # Настройки для yt-dlp
        yt_dlp_options = {
            'format': 'bestaudio/best',  # Лучшее качество аудио
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),  # Шаблон имени файла
            'postprocessors': [{  # Конвертируем в MP3
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': str(bitrate),
            }],
            'quiet': True,  # Отключение лишних сообщений
        }

        try:
            loop = asyncio.get_event_loop()
            with yt_dlp.YoutubeDL(yt_dlp_options) as ydl:
                # Асинхронно скачиваем аудио
                info = await loop.run_in_executor(None, ydl.extract_info, url, True)
                # Получаем путь к скачанному файлу
                filename = ydl.prepare_filename(info)
                extension = Path(filename).suffix  # Вернёт ".jpg"
                mp3_filename = filename.replace(extension, ".mp3")
                return {'status': True, 'massage': mp3_filename}
        except Exception as e:
            return {'status': False, 'massage': f"Error: {e}"}


ytd_obj = YouTubeDownloader()
