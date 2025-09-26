from app import create_app


def test_index_returns_ok():
    app = create_app()
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"OK" in resp.data
