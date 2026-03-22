import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

HEADERS = {"Remote-User": "testuser"}


@pytest.mark.asyncio
async def test_create_language():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.post("/api/languages", json={"name": "Angličtina", "emoji": "🇬🇧"}, headers=HEADERS)
    assert resp.status_code == 201
    assert resp.json()["name"] == "Angličtina"


@pytest.mark.asyncio
async def test_list_languages():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/api/languages", headers=HEADERS)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_update_language():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        create_resp = await ac.post("/api/languages", json={"name": "Němčina"}, headers=HEADERS)
        lang_id = create_resp.json()["id"]
        resp = await ac.patch(f"/api/languages/{lang_id}", json={"name": "Němčina Updated"}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Němčina Updated"


@pytest.mark.asyncio
async def test_delete_language():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        create_resp = await ac.post("/api/languages", json={"name": "Španělština"}, headers=HEADERS)
        lang_id = create_resp.json()["id"]
        resp = await ac.delete(f"/api/languages/{lang_id}", headers=HEADERS)
    assert resp.status_code == 204
