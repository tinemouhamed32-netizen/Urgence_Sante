from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"


def test_root_endpoint() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Urgence Santé" in response.json()["message"]


def test_country_and_language_validation_keep_named_response_fields() -> None:
    country_response = client.get("/api/v1/validate-country", params={"country": "sn"})
    language_response = client.get("/api/v1/validate-language", params={"language": "FR"})

    assert country_response.status_code == 200
    assert country_response.json() == {"country": "SN", "valid": True}
    assert language_response.status_code == 200
    assert language_response.json() == {"language": "fr", "valid": True}


def test_openapi_documents_response_models_and_error_responses() -> None:
    openapi = client.get("/openapi.json").json()
    paths = openapi["paths"]

    assert paths["/api/v1/health-information/search"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "/HealthSearchResponse"
    )
    assert "400" in paths["/api/v1/health-information/search"]["get"]["responses"]
    assert "404" in paths["/api/v1/health-information/search"]["get"]["responses"]
    assert "422" in paths["/api/v1/assistant/message"]["post"]["responses"]
