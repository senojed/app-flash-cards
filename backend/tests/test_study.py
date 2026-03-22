import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

HEADERS = {"Remote-User": "testuser"}


async def _setup(ac):
    lang_resp = await ac.post("/api/languages", json={"name": "Angličtina"}, headers=HEADERS)
    lang_id = lang_resp.json()["id"]
    lesson_resp = await ac.post("/api/lessons", json={"language_id": lang_id, "name": "Lekce 1"}, headers=HEADERS)
    lesson_id = lesson_resp.json()["id"]
    card_resp = await ac.post("/api/cards", json={
        "lesson_id": lesson_id,
        "fields": [{"label": "front", "content": "Hello"}, {"label": "back", "content": "Ahoj"}]
    }, headers=HEADERS)
    card_id = card_resp.json()["id"]
    return lesson_id, card_id


@pytest.mark.asyncio
async def test_rate_card_updates_progress():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        lesson_id, card_id = await _setup(ac)

        study_resp = await ac.post("/api/study/cards", json={"lesson_ids": [lesson_id]}, headers=HEADERS)
        assert study_resp.status_code == 200
        cards = study_resp.json()
        assert len(cards) == 1

        rate_resp = await ac.post("/api/study/rate", json={
            "card_id": card_id,
            "direction": "front_to_back",
            "quality": 4,
        }, headers=HEADERS)
        assert rate_resp.status_code == 200
        data = rate_resp.json()
        assert data["new_interval"] == 1
        assert data["is_learned"] is False
        assert "previous_state" in data


@pytest.mark.asyncio
async def test_undo_reverts_progress():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        lesson_id, card_id = await _setup(ac)

        rate_resp = await ac.post("/api/study/rate", json={
            "card_id": card_id,
            "direction": "front_to_back",
            "quality": 4,
        }, headers=HEADERS)
        previous_state = rate_resp.json()["previous_state"]
        assert previous_state["is_new"] is True

        undo_resp = await ac.post("/api/study/undo", json=previous_state, headers=HEADERS)
        assert undo_resp.status_code == 204

        # Po undo jsou karty znovu k dispozici
        study_resp = await ac.post("/api/study/cards", json={"lesson_ids": [lesson_id]}, headers=HEADERS)
        assert len(study_resp.json()) == 1
