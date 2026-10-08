import pytest
from pydantic import ValidationError

from app.schemas import (
    HealthStatusResponse,
    ProbabilityBreakdown,
    TextDetectionRequest,
    TextDetectionResponse,
)


def test_text_detection_request_valid():
    req = TextDetectionRequest(text="  This is a legitimate test sentence for classification.  ")
    assert req.text == "This is a legitimate test sentence for classification."


def test_text_detection_request_too_short():
    with pytest.raises(ValidationError):
        TextDetectionRequest(text="abc")


def test_text_detection_request_whitespace_only():
    with pytest.raises(ValidationError):
        TextDetectionRequest(text="         ")


def test_text_detection_response_structure():
    data = {
        "verdict": "AI-Generated",
        "confidence": 95.5,
        "is_ai": True,
        "probabilities": {"human": 4.5, "ai": 95.5},
    }
    resp = TextDetectionResponse(**data)
    assert resp.verdict == "AI-Generated"
    assert resp.confidence == 95.5
    assert resp.is_ai is True
    assert resp.probabilities["ai"] == 95.5


def test_probability_breakdown_schema():
    pb = ProbabilityBreakdown(human=80.0, ai=20.0)
    assert pb.human == 80.0
    assert pb.ai == 20.0


def test_health_status_response():
    health = HealthStatusResponse(
        status="healthy",
        app="AI Text Detector",
        version="1.0.0",
        device="cpu",
        model_loaded=True,
    )
    assert health.status == "healthy"
    assert health.model_loaded is True
