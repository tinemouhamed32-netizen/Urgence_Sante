from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_information_search_returns_results() -> None:
    response = client.get("/api/v1/health-information/search", params={"q": "hydratation", "country": "SN", "language": "fr"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] >= 1
    result = next(item for item in payload["results"] if item["article_id"] == "hydration-01")
    assert result["status"] == "demo_only"
    assert result["source"] == "Contenu de démonstration non référencé"
    assert result["last_verified"] is None


def test_health_information_search_missing_result() -> None:
    response = client.get("/api/v1/health-information/search", params={"q": "traitement secret", "country": "SN", "language": "fr"})
    assert response.status_code == 404


def test_health_information_sources_endpoint() -> None:
    response = client.get("/api/v1/health-information/sources", params={"country": "SN", "language": "fr"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] >= 1
    assert any(item["name"] for item in payload["results"])


def test_health_information_rejects_blank_query() -> None:
    response = client.get("/api/v1/health-information/search", params={"q": "   ", "country": "SN", "language": "fr"})
    assert response.status_code == 400


def test_health_information_rejects_invalid_country_and_language() -> None:
    response = client.get("/api/v1/health-information/search", params={"q": "hydratation", "country": "SENEGAL", "language": "xx"})
    assert response.status_code == 400

    source_response = client.get("/api/v1/health-information/sources", params={"country": "SENEGAL", "language": "xx"})
    assert source_response.status_code == 400


def test_health_information_search_matches_common_paraphrases() -> None:
    hydration = client.get(
        "/api/v1/health-information/search",
        params={"q": "Comment boire davantage quand il fait chaud ?", "country": "SN", "language": "fr"},
    )
    sleep = client.get(
        "/api/v1/health-information/search",
        params={"q": "J'ai du mal à dormir", "country": "SN", "language": "fr"},
    )

    assert hydration.status_code == 200
    assert hydration.json()["results"][0]["article_id"] == "hydration-01"
    assert sleep.status_code == 200
    assert sleep.json()["results"][0]["article_id"] == "sleep-01"


def test_health_information_search_does_not_match_unrelated_questions() -> None:
    response = client.get(
        "/api/v1/health-information/search",
        params={"q": "Comment diagnostiquer le paludisme ?", "country": "SN", "language": "fr"},
    )

    assert response.status_code == 404


def test_assistant_labels_demo_answer_without_claiming_verified_sources() -> None:
    response = client.post(
        "/api/v1/assistant/message",
        json={"question": "Comment boire davantage quand il fait chaud ?", "country": "SN", "language": "fr"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["category"] == "general"
    assert any("non référencée et non vérifiée" in limitation for limitation in payload["limitations"])
