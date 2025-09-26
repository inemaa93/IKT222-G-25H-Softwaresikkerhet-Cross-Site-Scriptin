# XSS Demo (Flask + SQLite)

Bootstrap for the course assignment: full-stack app with an intentional XSS vuln (later) and mitigation.

## Quickstart (local)

```bash
python -m venv .venv
# mac/linux
source .venv/bin/activate
# windows powershell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt -r requirements-dev.txt
pytest
```

Run Flask dev server:
```bash
export FLASK_APP=app:create_app
flask run --debug
```

## Docker

```bash
docker build -t xss-demo .
docker run --rm -p 8000:8000 -v $(pwd)/instance:/app/instance xss-demo
# open http://localhost:8000
```

Or with Compose:
```bash
docker-compose up --build
```

## CI

GitHub Actions runs Ruff, Black (check), and pytest on pushes and PRs.
