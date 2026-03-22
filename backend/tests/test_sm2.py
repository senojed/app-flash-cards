import pytest
from app.services.sm2 import sm2_update, is_learned


def test_first_review_score_4():
    result = sm2_update(interval=1, ease_factor=2.5, repetitions=0, quality=4)
    assert result["interval"] == 1
    assert result["repetitions"] == 1
    assert result["ease_factor"] == pytest.approx(2.5, rel=0.01)


def test_second_review_score_4():
    result = sm2_update(interval=1, ease_factor=2.5, repetitions=1, quality=4)
    assert result["interval"] == 6
    assert result["repetitions"] == 2


def test_score_below_3_resets():
    result = sm2_update(interval=10, ease_factor=2.5, repetitions=5, quality=0)
    assert result["interval"] == 1
    assert result["repetitions"] == 0
    assert result["ease_factor"] == pytest.approx(2.5)


def test_ease_factor_minimum():
    result = sm2_update(interval=1, ease_factor=1.4, repetitions=3, quality=3)
    assert result["ease_factor"] >= 1.3


def test_learned_threshold():
    assert is_learned(interval=21, threshold=21) is True
    assert is_learned(interval=20, threshold=21) is False
