#!/usr/bin/env bash
set -e

# Change directory to project root
cd "$(dirname "$0")/.."

# Check if .env exists, if not copy from .env.example
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

# Activate virtualenv if present
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "Starting AI Text Detector development server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
