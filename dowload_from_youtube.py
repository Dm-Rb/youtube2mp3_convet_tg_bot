import yt_dlp
import asyncio


class YouTubeDownloader:

    validate_val = 'https://www.youtu'

    async def get_metadata(self, url):
        """Асинхронно получает метаданные видео."""
        if not url.startswith(self.validate_val):
            return {'status': False, 'massage': 'Некорректная ссылка'}

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


ytd_obj = YouTubeDownloader()