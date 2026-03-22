import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

HEADERS = {"Remote-User": "testuser"}


async def _setup(ac):
    lang_resp = await ac.post("/api/languages", json={"name": "Angličtina"}, headers=HEADERS)
    lang_id = lang_resp.json()["id"]
    lesson_resp = await ac.post("/api/lessons", json={"language_id": lang_id, "name": "Lekce 1"}, headers=HEADERS)
    return lesson_resp.json()["id"]


@pytest.mark.asyncio
async def test_import_csv():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        lesson_id = await _setup(ac)
        csv_content = b"front,back\nHello,Ahoj\nCat,Kocka"
        resp = await ac.post("/api/import", data={"lesson_id": lesson_id}, files={"file": ("test.csv", csv_content, "text/csv")}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["imported"] == 2
    assert resp.json()["skipped"] == 0


@pytest.mark.asyncio
async def test_import_skips_duplicates():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        lesson_id = await _setup(ac)
        csv_content = b"front,back\nHello,Ahoj\nCat,Kocka"
        await ac.post("/api/import", data={"lesson_id": lesson_id}, files={"file": ("test.csv", csv_content, "text/csv")}, headers=HEADERS)
        resp = await ac.post("/api/import", data={"lesson_id": lesson_id}, files={"file": ("test.csv", csv_content, "text/csv")}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["imported"] == 0
    assert resp.json()["skipped"] == 2
