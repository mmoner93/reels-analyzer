from celery import Celery, chain
from pathlib import Path
import shutil

from api.config import settings
from api.database import SessionLocal
from api.models import Task, TaskStatus

from .downloader import DownloaderService
from .audio_extractor import AudioExtractorService
from .transcriber import TranscriberService
from .text_analyzer import TextAnalyzerService

celery_app = Celery(
    "reels_processor",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task(bind=True)
def process_reel_task(self, task_id: int):
    """Main task to process a reel through the entire pipeline."""
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return {"error": "Task not found"}
        
        if task.status == TaskStatus.CANCELLED:
            return {"status": "cancelled"}
        
        # Update status to processing
        task.status = TaskStatus.PROCESSING
        db.commit()
        
        # Step 1: Download video
        downloader = DownloaderService(settings.temp_dir)
        video_path = downloader.download_reel(task.url, task_id)
        
        if task.status == TaskStatus.CANCELLED:
            cleanup_temp_files(task_id)
            return {"status": "cancelled"}
        
        # Step 2: Extract audio
        extractor = AudioExtractorService()
        audio_path = extractor.extract_audio(video_path)
        
        if task.status == TaskStatus.CANCELLED:
            cleanup_temp_files(task_id)
            return {"status": "cancelled"}
        
        # Step 3: Transcribe
        transcriber = TranscriberService()
        transcript = transcriber.transcribe(audio_path)
        task.transcript = transcript
        db.commit()
        
        if task.status == TaskStatus.CANCELLED:
            cleanup_temp_files(task_id)
            return {"status": "cancelled"}
        
        # Step 4: Analyze text (bonus feature)
        analyzer = TextAnalyzerService()
        language = analyzer.detect_language(transcript)
        topics = analyzer.extract_topics(transcript)
        
        task.language = language
        task.topics = ", ".join(topics)
        task.status = TaskStatus.COMPLETED
        db.commit()
        
        # Cleanup temp files
        cleanup_temp_files(task_id)
        
        return {
            "status": "completed",
            "transcript": transcript,
            "language": language,
            "topics": topics
        }
        
    except Exception as e:
        task.status = TaskStatus.FAILED
        task.error_message = str(e)
        db.commit()
        cleanup_temp_files(task_id)
        raise
    finally:
        db.close()


def cleanup_temp_files(task_id: int):
    """Clean up temporary files for a task."""
    temp_path = Path(settings.temp_dir) / f"task_{task_id}"
    if temp_path.exists():
        shutil.rmtree(temp_path)
