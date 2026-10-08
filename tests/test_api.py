from unittest.mock import patch
from fastapi.testclient import TestClient


def test_serve_frontend(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert "AI Text Detection" in response.text or "<!DOCTYPE html>" in response.text


def test_health_check_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "app" in data
    assert "version" in data
    assert "device" in data
    assert "model_loaded" in data


def test_detect_endpoint_validation_error_short_text(client: TestClient):
    response = client.post("/api/v1/detect", json={"text": "hi"})
    assert response.status_code == 422


def test_detect_endpoint_validation_error_empty(client: TestClient):
    response = client.post("/api/v1/detect", json={"text": "   "})
    assert response.status_code == 422


def test_detect_endpoint_success_mocked(client: TestClient):
    mock_detection_result = {
        "verdict": "AI-Generated",
        "confidence": 92.5,
        "is_ai": True,
        "probabilities": {"human": 7.5, "ai": 92.5},
    }
    with patch("app.services.detector.detector_service.is_loaded", True), \
         patch("app.services.detector.detector_service.detect", return_value=mock_detection_result):
        response = client.post(
            "/api/v1/detect",
            json={"text": "This is a synthetic paragraph created to test the detection service."}
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["verdict"] == "AI-Generated"
        assert payload["confidence"] == 92.5
        assert payload["is_ai"] is True
        assert payload["probabilities"]["ai"] == 92.5


def test_detect_endpoint_service_unavailable_when_unloaded(client: TestClient):
    with patch("app.services.detector.detector_service.is_loaded", False):
        response = client.post(
            "/api/v1/detect",
            json={"text": "Testing behavior when detector service is not loaded."}
        )
        assert response.status_code == 503
        assert "unavailable" in response.json()["detail"].lower()
