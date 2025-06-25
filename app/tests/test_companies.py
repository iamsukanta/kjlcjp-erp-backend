from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_companies():
    res = client.post("/api/v1/companies/", json={"name": "TestCorp", "type": "tech"})
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "TestCorp"

    res = client.get("/api/v1/companies/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
