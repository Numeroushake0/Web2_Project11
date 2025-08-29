import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_create_contact():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/contacts/", json={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "987654321",
            "birthday": "1995-05-05"
        })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["email"] == "jane@example.com"


@pytest.mark.asyncio
async def test_get_contacts():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/contacts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
