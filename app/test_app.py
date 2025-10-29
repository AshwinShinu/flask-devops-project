import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Check if home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200

def test_api_students(client):
    """Check if API returns JSON list"""
    response = client.get('/api/students')
    assert response.status_code == 200
    assert isinstance(response.json, list)
