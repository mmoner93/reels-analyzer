import ffmpeg
from pathlib import Path


class AudioExtractorService:
    def extract_audio(self, video_path: str) -> str:
        """Extract audio from video and return path to audio file."""
        video_path_obj = Path(video_path)
        audio_path = video_path_obj.parent / "audio.wav"
        
        stream = ffmpeg.input(video_path)
        stream = ffmpeg.output(stream, str(audio_path), acodec='pcm_s16le', ac=1, ar='16k')
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
        
        return str(audio_path)
