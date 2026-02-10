import whisper
from pathlib import Path


class TranscriberService:
    def __init__(self):
        self.model = None
    
    def load_model(self):
        """Load Whisper model (lazy loading)."""
        if self.model is None:
            self.model = whisper.load_model("base")
    
    def transcribe(self, audio_path: str) -> str:
        """Transcribe audio file and return text."""
        self.load_model()
        result = self.model.transcribe(audio_path, fp16=False)
        return result["text"]
