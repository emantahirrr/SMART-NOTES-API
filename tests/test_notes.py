import pytest
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_user_cannot_access_others_note():
    user_a = {"username": "a@example.com", "email": "a@example.com", "password": "password123"}
    user_b = {"username": "b@example.com", "email": "b@example.com", "password": "password123"}
    for user_data in [user_a, user_b]:
        reg = client.post("/register", json=user_data)
        if reg.status_code == 422:
            print(f"\n[DEBUG] Registration Validation Error: {reg.json()}")
        assert reg.status_code in [200, 201], f"Registration failed: {reg.text}"
    resp_a = client.post("/token", data={"username": user_a["email"], "password": user_a["password"]})
    assert resp_a.status_code == 200, f"Login failed for User A: {resp_a.json()}"
    token_a = resp_a.json()["access_token"]
    note_resp = client.post(
        "/notes", 
        json={"title": "Secret", "content": "Only A should see this"},
        headers={"Authorization": f"Bearer {token_a}"}
    )
    assert note_resp.status_code in [200, 201]
    note_id = note_resp.json()["id"]
    resp_b = client.post("/token", data={"username": user_b["email"], "password": user_b["password"]})
    token_b = resp_b.json()["access_token"]
    response = client.get(f"/notes/{note_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert response.status_code in [403, 404], f"Security failure! User B accessed User A's note. Status: {response.status_code}"