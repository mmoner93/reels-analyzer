import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from api.main import app
from api.database import Base, engine
from api.models import Task, TaskStatus

@pytest.fixture
def client():
    # Create test database
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # Clean up
    Base.metadata.drop_all(bind=engine)


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@patch('api.routes.process_reel_task')
def test_create_task(mock_task, client):
    mock_task.delay = MagicMock(return_value=None)
    
    response = client.post(
        "/api/tasks",
        json={"url": "https://www.instagram.com/reel/test"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["url"] == "https://www.instagram.com/reel/test"
    assert data["status"] == "pending"


@patch('api.routes.process_reel_task')
def test_list_tasks(mock_task, client):
    mock_task.delay = MagicMock(return_value=None)
    
    # Create a task first
    client.post("/api/tasks", json={"url": "https://www.instagram.com/reel/test1"})
    client.post("/api/tasks", json={"url": "https://www.instagram.com/reel/test2"})
    
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@patch('api.routes.process_reel_task')
def test_get_task(mock_task, client):
    mock_task.delay = MagicMock(return_value=None)
    
    # Create a task
    create_response = client.post(
        "/api/tasks",
        json={"url": "https://www.instagram.com/reel/test"}
    )
    task_id = create_response.json()["id"]
    
    # Get the task
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id


def test_get_nonexistent_task(client):
    response = client.get("/api/tasks/999")
    assert response.status_code == 404


@patch('api.routes.process_reel_task')
def test_cancel_task(mock_task, client):
    mock_task.delay = MagicMock(return_value=None)
    
    # Create a task
    create_response = client.post(
        "/api/tasks",
        json={"url": "https://www.instagram.com/reel/test"}
    )
    task_id = create_response.json()["id"]
    
    # Cancel the task
    response = client.patch(f"/api/tasks/{task_id}/cancel")
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"
