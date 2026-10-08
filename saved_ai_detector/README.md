# Saved AI Detector Model Artifacts

This directory contains configuration, tokenizer metadata, and model weights for the fine-tuned RoBERTa AI text detection classifier.

## Model Overview

- **Architecture:** `RobertaForSequenceClassification` (6 hidden layers, 12 attention heads, 768 hidden size)
- **Vocabulary Size:** 50,265 tokens
- **Max Sequence Length:** 512 tokens
- **Task:** Binary text classification
- **Classes:**
  - `0`: Human-Written
  - `1`: AI-Generated

## Artifact Files

| File | Description | Tracked in Git |
|------|-------------|----------------|
| `config.json` | Hugging Face model architecture and label mapping configuration | Yes |
| `tokenizer.json` | Tokenizer vocabulary and byte-level BPE configuration | Yes |
| `tokenizer_config.json` | Tokenizer metadata, special tokens, and padding rules | Yes |
| `model.safetensors` | Fine-tuned PyTorch model weights (~314 MB) | **No** (Excluded via `.gitignore`) |

## Model Weights Setup

Because GitHub imposes a strict 100 MB file size limit and storing binary weights in Git repositories is an anti-pattern:

1. `model.safetensors` is ignored by Git in `.gitignore`.
2. For local development or deployment, ensure `model.safetensors` is placed in this directory (`saved_ai_detector/model.safetensors`).
3. Alternatively, configure the custom path to the weights directory via the `MODEL_PATH` environment variable in `.env`.
