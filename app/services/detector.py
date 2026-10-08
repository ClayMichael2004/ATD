import logging
from pathlib import Path
from typing import Any, Optional

import torch
import torch.nn.functional as F
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from app.config import get_settings

logger = logging.getLogger(__name__)


class DetectionService:
    """Service handling text tokenization and model inference for AI text detection."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.tokenizer: Optional[AutoTokenizer] = None
        self.model: Optional[AutoModelForSequenceClassification] = None
        self.device: str = "cpu"
        self._is_loaded: bool = False

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    def determine_device(self) -> str:
        configured = self.settings.DEVICE.lower()
        if configured == "cuda" and torch.cuda.is_available():
            return "cuda"
        if configured == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return "cpu"

    def load_model(self) -> None:
        model_path = self.settings.resolved_model_path
        logger.info(f"Loading transformer model from: {model_path}")

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model directory '{model_path}' not found! "
                f"Ensure the model directory is placed at {model_path} or configure MODEL_PATH in .env"
            )

        self.device = self.determine_device()
        logger.info(f"Target execution device: {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(str(model_path), local_files_only=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            str(model_path), local_files_only=True
        ).to(self.device)
        self.model.eval()

        self._is_loaded = True
        logger.info(f"Model and tokenizer successfully loaded on device: {self.device}")

    def unload(self) -> None:
        self.tokenizer = None
        self.model = None
        self._is_loaded = False
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        logger.info("Model and tokenizer unloaded from memory.")

    def detect(self, text: str) -> dict[str, Any]:
        if not self._is_loaded or self.model is None or self.tokenizer is None:
            raise RuntimeError("Model is not loaded. Call load_model() before performing inference.")

        cleaned_text = text.strip()
        if not cleaned_text:
            raise ValueError("Input text cannot be empty.")

        inputs = self.tokenizer(
            cleaned_text,
            return_tensors="pt",
            truncation=True,
            max_length=self.settings.MAX_SEQUENCE_LENGTH,
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = F.softmax(logits, dim=-1)[0]

        prob_human = float(probs[0].item())
        prob_ai = float(probs[1].item())

        prediction_idx = int(torch.argmax(probs).item())
        confidence = prob_ai if prediction_idx == 1 else prob_human

        return {
            "verdict": "AI-Generated" if prediction_idx == 1 else "Human-Written",
            "confidence": round(confidence * 100, 2),
            "is_ai": bool(prediction_idx == 1),
            "probabilities": {
                "human": round(prob_human * 100, 2),
                "ai": round(prob_ai * 100, 2),
            },
        }


detector_service = DetectionService()
