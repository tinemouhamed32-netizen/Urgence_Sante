from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_information_search_returns_results() -> None:
    response = client.get("/api/v1/health-information/search", params={"q": "hydratation", "country": "SN", "language": "fr"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] >= 1


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
