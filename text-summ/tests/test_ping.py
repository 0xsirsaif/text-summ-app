from app import main


def test_ping(test_client):
    response = test_client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ENVIRONMENT": "dev", "TESTING": True, "ping": "saif!"}
