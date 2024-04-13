from fastapi.testclient import TestClient


def test_root(test_app: TestClient):
    response = test_app.get("/", follow_redirects=True)
    assert len(response.history) == 1
    assert response.status_code == 200
