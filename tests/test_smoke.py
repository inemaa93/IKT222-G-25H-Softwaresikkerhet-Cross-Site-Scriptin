from app import create_app
from app.db import init_db


def test_index_returns_ok(tmp_path):
    app = create_app()
    app.config.update(
        DATABASE=str(tmp_path / "test.db"),
        TESTING=True,
        SECRET_KEY="test",
    )

    # For å få til testen på GitHub legges dette til for å initiere testen
    with app.app_context():
        init_db()

    client = app.test_client()
    resp = client.get("/", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Posts" in resp.data
