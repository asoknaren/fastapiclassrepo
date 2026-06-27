import pytest

from simple_grader import build_grade_message, grade_from_score, is_passing


def test_grade_from_score_boundaries() -> None:
    assert grade_from_score(95) == "A"
    assert grade_from_score(85) == "B"
    assert grade_from_score(75) == "C"
    assert grade_from_score(65) == "D"
    assert grade_from_score(55) == "F"


def test_is_passing() -> None:
    assert is_passing(60) is True
    assert is_passing(59.9) is False


def test_build_grade_message() -> None:
    message = build_grade_message("Anita", 92)
    assert "Student: Anita" in message
    assert "Grade: A" in message
    assert "Status: PASS" in message


def test_invalid_score_raises_value_error() -> None:
    with pytest.raises(ValueError):
        grade_from_score(-1)

    with pytest.raises(ValueError):
        is_passing(101)
