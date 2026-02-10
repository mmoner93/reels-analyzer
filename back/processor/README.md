# Processor Module

Celery-based asynchronous processing pipeline for Instagram Reels.

## Structure

```
processor/
└── src/processor/
    ├── tasks.py            # Celery tasks orchestration
    ├── downloader.py       # Video download service
    ├── audio_extractor.py  # Audio extraction service
    ├── transcriber.py      # Speech-to-text service
    └── text_analyzer.py    # Text analysis service
```

## Running the Celery Worker

```bash
# From repository root
uv run celery -A processor.tasks worker --loglevel=info
```

## Processing Pipeline

1. **Download** (`DownloaderService`): Downloads video using yt-dlp
2. **Extract** (`AudioExtractorService`): Extracts audio track with ffmpeg
3. **Transcribe** (`TranscriberService`): Converts speech to text with Whisper
4. **Analyze** (`TextAnalyzerService`): Detects language and extracts topics

## Services

### DownloaderService
Downloads Instagram reels using yt-dlp.

```python
downloader = DownloaderService(temp_dir="./temp")
video_path = downloader.download_reel(url, task_id)
```

### AudioExtractorService
Extracts audio from video files.

```python
extractor = AudioExtractorService()
audio_path = extractor.extract_audio(video_path)
```

### TranscriberService
Transcribes audio to text using Whisper.

```python
transcriber = TranscriberService()
transcript = transcriber.transcribe(audio_path)
```

### TextAnalyzerService
Analyzes text for language and topics.

```python
analyzer = TextAnalyzerService()
language = analyzer.detect_language(transcript)
topics = analyzer.extract_topics(transcript)
```

## Testing

```bash
# Run processor tests
uv run pytest back/tests/src/tests/test_processor.py -v
```

## Configuration

Services can be configured via environment variables in the root `.env` file:

```env
TEMP_DIR=./temp
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```
