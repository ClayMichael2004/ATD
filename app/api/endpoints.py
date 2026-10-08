import logging
from fastapi import APIRouter, HTTPException, status

from app.schemas import TextDetectionRequest, TextDetectionResponse
from app.services.detector import detector_service

logger = logging.getLogger(__name__)

api_router = APIRouter(prefix="/api/v1", tags=["Detection"])


@api_router.post(
    "/detect",
    response_model=TextDetectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze text for AI generation patterns",
    description="Analyzes input text and returns classification verdict, confidence score, and probability distribution.",
)
def detect_ai_text(payload: TextDetectionRequest) -> TextDetectionResponse:
    if not detector_service.is_loaded:
        logger.error("Detection request received but detector model is not loaded.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Detection model is currently unavailable or initializing.",
        )

    try:
        result = detector_service.detect(payload.text)
        return TextDetectionResponse(**result)
    except ValueError as val_err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(val_err))
    except Exception as err:
        logger.exception("Unexpected error during text analysis")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(err)}",
        )
