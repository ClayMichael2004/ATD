# Contributing Guidelines

Thank you for your interest in contributing to the AI Text Detection Engine (ATD)!

## Code of Conduct

Please treat all members of the community with respect and empathy.

## Development Workflow

1. **Fork or Branch:** Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Virtual Environment:** Set up a local environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements-dev.txt
   ```
3. **Environment File:** Copy `.env.example` to `.env` and set local values. Do not commit `.env`.
4. **Git Best Practices:**
   - Never commit virtual environment directories (`venv/`).
   - Never commit `.env` or sensitive credentials.
   - Large model weights (`*.safetensors`, `*.pt`, `*.bin`) must remain in `.gitignore`.
5. **Testing:** Ensure all tests pass before submitting changes:
   ```bash
   pytest -v tests/
   ```
6. **Commit Messages:** Follow conventional commits:
   - `feat:` new feature
   - `fix:` bug fix
   - `docs:` documentation updates
   - `test:` test updates
   - `chore:` maintenance and tooling
