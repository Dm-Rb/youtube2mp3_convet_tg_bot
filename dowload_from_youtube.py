import yt_dlp
import asyncio
import os
import re
import logging


logger = logging.getLogger(__name__)


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
        try:
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
        except Exception as e:
            logger.error(
                f"method: get_metadata"
                f"URL: {url}, "
                f"Format: {format}, "
                f"Args: {locals()}, "
                f"Error type: {type(e).__name__}, "
                f"Error: {e}",
                exc_info=True  # traceback
            )

    async def download_video_extract_audio(self, url, bitrate):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': str(bitrate),
            }],
            'quiet': True,
            'noplaylist': True,
            # 'verbose': True,   # для отладки
        }

        try:
            loop = asyncio.get_running_loop()
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=True))

            # yt-dlp обычно создаёт файл с названием видео + .mp3
            expected_mp3 = os.path.join(self.output_dir, f"{info.get('title', 'unknown')}.mp3")

            # на случай экранирования или изменения символов ищем последний .mp3
            if not os.path.exists(expected_mp3):
                mp3_files = [f for f in os.listdir(self.output_dir) if f.lower().endswith('.mp3')]
                if mp3_files:
                    # берём самый новый по времени изменения
                    latest = max(mp3_files, key=lambda f: os.path.getmtime(os.path.join(self.output_dir, f)))
                    expected_mp3 = os.path.join(self.output_dir, latest)

            if os.path.exists(expected_mp3):
                return {'status': True, 'message': expected_mp3}
            else:
                return {'status': False, 'message': 'File .mp3 not found after download'}

        except Exception as e:
            logger.error(
                f"method: download_video_extract_audio"
                f"URL: {url}, "
                f"Format: {format}, "
                f"Args: {locals()}, "
                f"Error type: {type(e).__name__}, "
                f"Error: {e}",
                exc_info=True  # traceback
            )


ytd_obj = YouTubeDownloader()
