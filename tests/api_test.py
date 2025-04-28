from fastapi.testclient import TestClient

from app import app  # Change to absolute import

client = TestClient(app)

def test_home_page():
    """Test the home page returns correctly"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Compound Interest Calculator" in response.text

def test_calculate_endpoint():
    """Test the calculate endpoint with valid data"""
    data = {
        "principal": 1000,
        "rate": 5,
        "time": 1,
        "compounds_per_year": 12,
        "monthly_addition": 100
    }
    response = client.post("/calculate", data=data)
    assert response.status_code == 200
    assert "Calculation Results" in response.text
    assert "Tax Calculation (Netherlands)" in response.text

def test_calculate_endpoint_invalid_data():
    """Test the calculate endpoint with invalid data"""
    data = {
        "principal": -1000,  # Invalid negative value
        "rate": 5,
        "time": 1,
        "compounds_per_year": 12,
        "monthly_addition": 100
    }
    response = client.post("/calculate", data=data)
    assert response.status_code == 500
    assert "An error occurred" in response.text