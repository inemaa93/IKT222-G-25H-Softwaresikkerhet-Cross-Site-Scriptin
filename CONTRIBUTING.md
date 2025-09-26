## Dev Setup
- Python 3.12 + venv
- `pip install -r requirements.txt -r requirements-dev.txt`

## Conventions
- Branches: feat/*, fix/*, chore/*, docs/*
- Run locally before push:
  - `ruff check .`
  - `black .`
  - `pytest`
- All changes via PR with at least 1 review.
