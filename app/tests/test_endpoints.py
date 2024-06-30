from fastapi import Request, Response, status
from fastapi.testclient import TestClient
from ..main import app


client = TestClient(app)


def test_get_home():
    response: Response = client.get("/")
    
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["Content-Type"]
    

def test_post_home():
    response: Response = client.post("/")
    
    assert response.status_code == status.HTTP_200_OK
    assert "application/json" in response.headers["Content-Type"]
    assert response.json() == {"message": "Welcome to the FastAPI application! POST"}