import yt_dlp
import asyncio
import os


class YouTubeDownloader:

    validate_val = 'https://www.youtu'
    output_dir = os.path.join('.', 'downloads')

    def __init__(self):
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

    async def get_metadata(self, url):
        """Асинхронно получает метаданные видео."""
        if not url.startswith(self.validate_val):
            return {'status': False, 'massage': 'Некорректная ссылка'}
        #  "cookiefile": "cookies.txt"
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

    async def download_video_extract_audio(self, url):
        # Настройки для yt-dlp
        yt_dlp_options = {
            'format': 'bestaudio/best',  # Лучшее качество аудио
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),  # Шаблон имени файла
            'postprocessors': [{  # Конвертируем в MP3
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
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
                mp3_filename = filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")
                return mp3_filename
        except Exception as e:
            print(f"Ошибка при скачивании аудио: {e}")
            return None


ytd_obj = YouTubeDownloader()

# print(ytd_obj.download_video_extract_audio('https://www.youtube.com/watch?v=69RdQFDuYPI'))
