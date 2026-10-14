from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_emergency_protocols() -> None:
    response = client.get("/api/v1/emergency/protocols")
    assert response.status_code == 200
    payload = response.json()
    assert payload
    assert payload[0]["is_demo"] is True


def test_emergency_session_and_answer() -> None:
    start = client.post("/api/v1/emergency/session", json={"country": "SN", "language": "fr"})
    assert start.status_code == 200
    session_id = start.json()["session_id"]
    assert "démonstration fictive" in start.json()["guidance"].lower()

    answer = client.post(f"/api/v1/emergency/session/{session_id}/answer", json={"answer": "oui"})
    assert answer.status_code == 200
    assert answer.json()["status"] == "requires_immediate_help"
    assert "secours locaux" in answer.json()["guidance"].lower()
    assert "protocole validé" not in answer.json()["guidance"].lower()


def test_assistant_emergency_response_does_not_claim_to_triage() -> None:
    response = client.post(
        "/api/v1/assistant/message",
        json={"question": "C'est une urgence réelle", "country": "SN", "language": "fr"},
    )
    assert response.status_code == 200
    assert "ne réalise pas de triage médical" in response.json()["answer"].lower()
    assert "services de secours locaux" in response.json()["answer"].lower()
