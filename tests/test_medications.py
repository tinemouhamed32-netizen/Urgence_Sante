from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_medication_recognition_rejects_invalid_image() -> None:
    response = client.post(
        "/api/v1/medications/recognize",
        json={"file_name": "notes.txt", "content_type": "text/plain", "size_bytes": 10},
    )
    assert response.status_code == 400


def test_medication_recognition_accepts_demo_payload() -> None:
    response = client.post(
        "/api/v1/medications/recognize",
        json={"file_name": "medoc.jpg", "content_type": "image/jpeg", "size_bytes": 2048},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["requires_confirmation"] is True
    assert len(payload["candidates"]) >= 2
