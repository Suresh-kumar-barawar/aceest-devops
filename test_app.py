import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# ── HOME ─────────────────────────────────────────────────────────────────────

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "running"
    assert "message" in data

# ── PROGRAMS ──────────────────────────────────────────────────────────────────

def test_get_programs(client):
    response = client.get("/programs")
    assert response.status_code == 200
    data = response.get_json()
    assert "programs" in data
    assert len(data["programs"]) == 3

def test_get_valid_program(client):
    response = client.get("/program/Fat Loss (FL)")
    assert response.status_code == 200
    data = response.get_json()
    assert "details" in data
    assert "workout" in data["details"]
    assert "diet" in data["details"]

def test_get_invalid_program(client):
    response = client.get("/program/InvalidProgram")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

# ── CALORIES ──────────────────────────────────────────────────────────────────

def test_calculate_calories_valid(client):
    response = client.post("/calories", json={
        "weight": 70,
        "program": "Fat Loss (FL)"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["calories"] == 1540
    assert data["weight"] == 70

def test_calculate_calories_missing_fields(client):
    response = client.post("/calories", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_calculate_calories_invalid_program(client):
    response = client.post("/calories", json={
        "weight": 70,
        "program": "Unknown"
    })
    assert response.status_code == 404

def test_calculate_calories_invalid_weight(client):
    response = client.post("/calories", json={
        "weight": -10,
        "program": "Fat Loss (FL)"
    })
    assert response.status_code == 400

# ── CLIENTS ───────────────────────────────────────────────────────────────────

def test_add_client(client):
    response = client.post("/clients", json={
        "name": "Arjun",
        "age": 25,
        "weight": 75,
        "program": "Muscle Gain (MG)",
        "adherence": 80
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "Arjun" in data["message"]

def test_add_duplicate_client(client):
    client.post("/clients", json={"name": "Arjun", "age": 25})
    response = client.post("/clients", json={"name": "Arjun", "age": 25})
    assert response.status_code == 409
    data = response.get_json()
    assert "error" in data

def test_add_client_missing_name(client):
    response = client.post("/clients", json={"age": 25})
    assert response.status_code == 400

def test_get_all_clients(client):
    client.post("/clients", json={"name": "Priya", "age": 22})
    response = client.get("/clients")
    assert response.status_code == 200
    data = response.get_json()
    assert "clients" in data

def test_get_specific_client(client):
    client.post("/clients", json={"name": "Karthik", "age": 30})
    response = client.get("/clients/Karthik")
    assert response.status_code == 200
    data = response.get_json()
    assert "client" in data

def test_get_nonexistent_client(client):
    response = client.get("/clients/Nobody")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data