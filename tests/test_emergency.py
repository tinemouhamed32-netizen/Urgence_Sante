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


def test_assistant_escalates_unconscious_patient_with_first_aid_sources() -> None:
    response = client.post(
        "/api/v1/assistant/message",
        json={"question": "Un patient est inconscient que dois-je faire ?", "country": "SN", "language": "fr"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["category"] == "emergency"
    assert "appelle immédiatement le samu" in payload["answer"].lower()
    assert "respire normalement" in payload["answer"].lower()
    assert "n'attends pas une réponse de l'application" in " ".join(payload["limitations"]).lower()
    assert any("sja.org.uk/first-aid-advice/cpr/" in source for source in payload["sources"])
    assert any("samu.sn/contact" in source for source in payload["sources"])


def test_assistant_escalates_common_unconsciousness_phrasings() -> None:
    response = client.post(
        "/api/v1/assistant/message",
        json={"question": "Il ne se réveille pas et ne répond pas", "country": "SN", "language": "fr"},
    )

    assert response.status_code == 200
    assert response.json()["category"] == "emergency"
    assert "appelle immédiatement le samu" in response.json()["answer"].lower()


def test_assistant_other_emergencies_direct_to_local_services() -> None:
    response = client.post(
        "/api/v1/assistant/message",
        json={"question": "C'est une urgence réelle", "country": "SN", "language": "fr"},
    )
    assert response.status_code == 200
    assert "appelle immédiatement" in response.json()["answer"].lower()
    assert "ne doit pas retarder l'appel aux secours" in response.json()["answer"].lower()
