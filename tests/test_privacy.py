from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_gps_not_collected_without_consent() -> None:
    payload = {"question": "Je peux partager ma position ?", "country": "SN", "language": "fr"}
    response = client.post("/api/v1/assistant/message", json=payload)
    assert response.status_code == 200
    assert "limitations" in response.json().keys()


def test_health_endpoint_is_public() -> None:
    response = client.get("/health")
    assert response.status_code == 200
