from fastapi.testclient import TestClient

from grade_api import app


client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Class Grade Validation API is running"}


def test_validate_single_grade_success() -> None:
    payload = {"student_name": "Anita", "course": "Math", "score": 88}

    response = client.post("/grades/validate", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "student_name": "Anita",
        "course": "Math",
        "score": 88.0,
        "letter_grade": "B",
        "passed": True,
        "is_valid": True,
    }


def test_validate_single_grade_invalid_score() -> None:
    payload = {"student_name": "Anita", "course": "Math", "score": 120}

    response = client.post("/grades/validate", json=payload)

    assert response.status_code == 422


def test_validate_batch_success() -> None:
    payload = {
        "grades": [
            {"student_name": "A", "course": "Math", "score": 95},
            {"student_name": "B", "course": "Math", "score": 61},
            {"student_name": "C", "course": "Math", "score": 45},
        ]
    }

    response = client.post("/grades/validate/batch", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["total_students"] == 3
    assert data["pass_count"] == 2
    assert data["fail_count"] == 1
    assert data["results"][0]["letter_grade"] == "A"
    assert data["results"][1]["letter_grade"] == "D"
    assert data["results"][2]["letter_grade"] == "F"


def test_validate_batch_empty_list_rejected() -> None:
    response = client.post("/grades/validate/batch", json={"grades": []})

    assert response.status_code == 422
