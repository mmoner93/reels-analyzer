import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch
from api.main import app
from api.database import init_db

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    init_db()

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest.mark.asyncio
async def test_auth_flow(client):
    # Mock celery task to avoid Redis connection
    with patch("api.routes.process_reel_task.delay") as mock_delay:
        # 1. Register User A
        user_a = {"username": "userA", "password": "passwordA"}
        response = await client.post("/api/auth/register", json=user_a)
        if response.status_code == 400 and "already registered" in response.text:
            pass
        else:
            assert response.status_code == 201, f"Failed to register User A: {response.text}"

        # 2. Login User A
        login_data_a = {"username": "userA", "password": "passwordA"}
        response = await client.post("/api/auth/token", data=login_data_a)
        assert response.status_code == 200, f"Failed to login User A: {response.text}"
        token_a = response.json()["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        # 3. Create Task as User A
        task_data = {"url": "https://instagram.com/reel/123"}
        response = await client.post("/api/tasks", json=task_data, headers=headers_a)
        assert response.status_code == 201, f"Failed to create task for User A: {response.text}"
        task_id = response.json()["id"]

        # Verify mock called
        mock_delay.assert_called_with(task_id)

        # 4. Verify Task is listed for User A
        response = await client.get("/api/tasks", headers=headers_a)
        assert response.status_code == 200
        tasks_a = response.json()
        assert len(tasks_a) >= 1
        assert any(t["id"] == task_id for t in tasks_a)

        # 5. Register User B
        user_b = {"username": "userB", "password": "passwordB"}
        response = await client.post("/api/auth/register", json=user_b)
        if response.status_code == 400 and "already registered" in response.text:
            pass
        else:
            assert response.status_code == 201

        # 6. Login User B
        login_data_b = {"username": "userB", "password": "passwordB"}
        response = await client.post("/api/auth/token", data=login_data_b)
        assert response.status_code == 200
        token_b = response.json()["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # 7. Verify Task is NOT listed for User B
        response = await client.get("/api/tasks", headers=headers_b)
        assert response.status_code == 200
        tasks_b = response.json()
        assert not any(t["id"] == task_id for t in tasks_b), "User B sees User A's task!"

        # 8. Verify User B cannot access User A's task specifically
        response = await client.get(f"/api/tasks/{task_id}", headers=headers_b)
        assert response.status_code == 404, "User B accessed User A's task!"
