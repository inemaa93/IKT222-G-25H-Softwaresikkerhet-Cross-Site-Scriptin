from app import create_app


def test_index_returns_ok():
    app = create_app()
    client = app.test_client()
    resp = client.get("/", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Posts" in resp.data
