import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_no_auth_required():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/api/health")
    assert resp.status_code == 200

@pytest.mark.asyncio
async def test_protected_endpoint_without_header_returns_401():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/api/me")
    assert resp.status_code == 401

@pytest.mark.asyncio
async def test_protected_endpoint_with_header_returns_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/api/me", headers={"Remote-User": "testuser"})
    assert resp.status_code == 200
    assert resp.json()["username"] == "testuser"
