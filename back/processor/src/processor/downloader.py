import os
import yt_dlp
from pathlib import Path


class DownloaderService:
    def __init__(self, temp_dir: str = "./temp"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(exist_ok=True)
    
    def download_reel(self, url: str, task_id: int) -> str:
        """Download Instagram reel and return the path to the downloaded file."""
        output_path = self.temp_dir / f"task_{task_id}"
        output_path.mkdir(exist_ok=True)
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': str(output_path / 'video.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        return filename
