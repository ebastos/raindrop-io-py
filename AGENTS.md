# AGENTS.md - Raindrop-io-py

This document provides essential guidance for GenAI coding assistants working on the `raindrop-io-py` codebase.

## Project Overview
- **Purpose**: A Pythonic wrapper for the [Raindrop.io](https://raindrop.io) API (v0.4.7).
- **Architecture**: A two-tier design separating HTTP transport ([api.py](file:///Users/main/src/raindrop-io-py/raindropiopy/api.py)) from domain models ([models.py](file:///Users/main/src/raindrop-io-py/raindropiopy/models.py)).
- **Patterns**:
  - **Active Record**: Models (e.g., `Raindrop`, `Collection`) encapsulate both data and CRUD logic.
  - **Context Manager**: The `API` class manages the connection lifecycle.
  - **Pydantic**: Used for data validation and serialization of API responses.

## Dev Environment Tips
- **Package Manager**: Always use `uv`.
- **Sync Environment**: Run `uv sync` to ensure your virtual environment matches `pyproject.toml`.
- **Locate Package**: Use `uv run python -c "import raindropiopy; print(raindropiopy.__file__)"` to find where the package is installed.
- **Environment Variables**: Requires `RAINDROP_TOKEN` (see `.env` or `README.md`).
- **Task Runners**: Use `just` (via `justfile`) or `poe` (via `pyproject.toml`) for common tasks.

## Key Commands & Workflows
- **Sync Dependencies**: `uv sync`
- **Linting**: `uv run ruff check .`
- **Formatting**: `uv run ruff format .` (Ruff handles both linting and formatting)
- **Dead Code Analysis**: `uv run vulture .` (uses `vulture_whitelist.py`)
- **Type Checking**: While not currently enforced in CI, aim for compatibility with `pyright` or `mypy`.
- **Release Automation**: Tasks like `poe BUILD`, `poe RELEASE`, and `poe VERSION` are defined in `pyproject.toml`.

## Testing Instructions
- **Framework**: `pytest`.
- **API Mocking**: Uses `vcrpy`. Cassettes are stored in `tests/api/cassettes/`.
- **Run All Tests**: `uv run pytest`
- **Run Specific Test**: `uv run pytest tests/api/test_models_raindrop.py`
- **Recording Cassettes**: Set `RAINDROP_VCR_RECORD=all` to record new cassettes (requires live credentials).
- **Policy**: NEVER make live API calls in automated tests without VCR unless explicitly directed.

## Constraints & Conventions
- **Python Version**: Supports Python 3.10 to <4.0.
- **Style**: Enforce Google-style docstrings for all public methods.
- **Data Integrity**: All API responses MUST be mapped to Pydantic models in `models.py`.
- **Separation of Concerns**: Keep HTTP-specific logic in `api.py` and domain logic in `models.py`.
- **Modern Python**: Use 3.10+ type hinting (e.g., `str | None` instead of `Optional[str]`).

## PR Instructions
- **Title Format**: `[raindrop-io-py] <Brief Description>`
- **Pre-Commit**: Always run `uv run ruff check .` and `uv run pytest` before committing.
- **Documentation**: If adding public methods, update Sphinx documentation in the `docs/` directory.
