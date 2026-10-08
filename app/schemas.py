from pydantic import BaseModel, Field, field_validator


class TextDetectionRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=5,
        max_length=10000,
        description="The text snippet to analyze for AI-generated patterns",
        examples=["In recent years, artificial intelligence has made significant strides in natural language processing."]
    )

    @field_validator("text")
    @classmethod
    def validate_non_whitespace(cls, v: str) -> str:
        stripped = v.strip()
        if len(stripped) < 5:
            raise ValueError("Text content must contain at least 5 non-whitespace characters.")
        return stripped


class ProbabilityBreakdown(BaseModel):
    human: float = Field(..., ge=0.0, le=100.0, description="Probability percentage of human authorship")
    ai: float = Field(..., ge=0.0, le=100.0, description="Probability percentage of AI authorship")


class TextDetectionResponse(BaseModel):
    verdict: str = Field(..., description="Classification verdict: 'AI-Generated' or 'Human-Written'")
    confidence: float = Field(..., ge=0.0, le=100.0, description="Confidence score percentage of the predicted label")
    is_ai: bool = Field(..., description="Boolean flag indicating whether the text is classified as AI-generated")
    probabilities: dict[str, float] = Field(..., description="Breakdown of human and AI probabilities")

    model_config = {
        "json_schema_extra": {
            "example": {
                "verdict": "AI-Generated",
                "confidence": 98.42,
                "is_ai": True,
                "probabilities": {
                    "human": 1.58,
                    "ai": 98.42
                }
            }
        }
    }


class HealthStatusResponse(BaseModel):
    status: str
    app: str
    version: str
    device: str
    model_loaded: bool