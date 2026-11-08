# Contributing to Game Title Researcher

Thank you for your interest in contributing to **Game Title Researcher**! We welcome contributions from developers, game researchers, and AI agents.

## Code of Conduct

Please maintain a respectful, welcoming, and constructive environment for all contributors.

## How to Contribute

### 1. Reporting Bugs
- Search existing issues to ensure the bug hasn't already been reported.
- Open a new issue with a clear description, reproduction steps, expected vs actual behavior, and system environment (OS, Python version).

### 2. Suggesting Storefront Adapters or Features
- We prioritize **keyless, public APIs and endpoints** to ensure zero-barrier usage.
- If proposing an adapter requiring an API key, it must have graceful fallback when no credentials exist.

### 3. Submitting Pull Requests
1. Fork the repository and create your branch from `main`:
   ```bash
   git checkout -b feature/my-new-feature
   ```
2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
3. Write clean, readable Python (Python 3.10+):
   - Include type annotations (`from __future__ import annotations`).
   - Follow PEP 8 guidelines.
4. Add or update tests in `tests/`:
   ```bash
   python -m pytest tests/ -v
   ```
   Ensure all tests pass before opening a PR.
5. Push to your fork and submit a Pull Request describing your changes.

## Development Setup

```bash
git clone https://github.com/mahmutbaysag/game-title-researcher.git
cd game-title-researcher
python -m venv .venv
# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

pip install -r requirements-dev.txt
python -m pytest tests/
```

## License

By contributing to Game Title Researcher, you agree that your contributions will be licensed under its [MIT License](LICENSE).
