from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from processor.tasks import process_reel_task

from api.database import get_db
from api.models import Task, TaskStatus
from api.schemas import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    """Create a new processing task."""
    task = Task(url=task_data.url, status=TaskStatus.PENDING)
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # Trigger async processing
    process_reel_task.delay(task.id)
    
    return task


@router.get("", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    """List all tasks."""
    tasks = db.query(Task).order_by(Task.created_at.desc()).all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task by ID."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}/cancel", response_model=TaskResponse)
def cancel_task(task_id: int, db: Session = Depends(get_db)):
    """Cancel a task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot cancel task with status: {task.status}"
        )
    
    task.status = TaskStatus.CANCELLED
    db.commit()
    db.refresh(task)
    return task


@router.get("/{task_id}/transcript")
def get_transcript(task_id: int, db: Session = Depends(get_db)):
    """Get the transcript for a completed task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status != TaskStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail=f"Transcript not available. Task status: {task.status}"
        )
    
    return {
        "id": task.id,
        "transcript": task.transcript,
        "language": task.language,
        "topics": task.topics
    }
