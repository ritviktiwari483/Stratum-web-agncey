import pytest
from main import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home endpoint"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.json == {"status": "ok"}

def test_contact_validation(client):
    """Test that contact endpoint requires name and email"""
    rv = client.post('/api/contact', json={})
    assert rv.status_code == 400
    assert "Name and email required" in rv.json['message']

def test_contact_submission(client):
    """Test successful contact submission"""
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "+911234567890",
        "message": "Hello, this is a test message."
    }
    rv = client.post('/api/contact', json=payload)
    assert rv.status_code == 200
    assert rv.json['status'] == "success"
    assert "Thanks!" in rv.json['message']

def test_admin_page(client):
    """Test that admin page loads"""
    rv = client.get('/admin')
    assert rv.status_code == 200
    assert b"Leads" in rv.data
