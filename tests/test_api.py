# tests/test_api.py
import os, tempfile
os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.mkdtemp()}/test.db"

import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:      # "with" is required so lifespan creates the tables
        yield c

RECIPE = {"title": "Pho Bo Hanoi", "summary": "A classic beef noodle soup recipe.",
          "category": "soups", "minutes": 120, "servings": 4,
          "ingredients": [{"qty": "500g", "item": "beef"}],
          "steps": [{"title": "Boil", "text": "Boil bones"}]}

def register(client, name="alice"):
    return client.post("/api/auth/register", json={
        "email": f"{name}@x.com", "username": name,
        "password": "password123", "display_name": name.title()})

def test_protected_needs_login(client):
    assert client.post("/api/recipes", json=RECIPE).status_code == 401

def test_register_duplicate(client):
    assert register(client).status_code == 201
    assert register(client).status_code == 409

def test_validation_422(client):
    bad = {**RECIPE, "category": "pizza"}
    assert client.post("/api/recipes", json=bad).status_code == 422

def test_recipe_lifecycle(client):
    r = client.post("/api/recipes", json=RECIPE)
    assert r.status_code == 201
    rid = r.json()["id"]
    assert client.get(f"/api/recipes/{rid}").json()["ingredients"][0]["item"] == "beef"
    assert client.get("/api/recipes?q=pho").json()["total"] >= 1

def test_review_updates_rating(client):
    rid = client.get("/api/recipes").json()["items"][0]["id"]
    client.post(f"/api/recipes/{rid}/reviews", json={"rating": 5, "comment": "great"})
    client.post(f"/api/recipes/{rid}/reviews", json={"rating": 3, "comment": "ok now"})  # updates, not duplicates
    assert client.get(f"/api/recipes/{rid}/reviews").json().__len__() == 1
    assert client.get(f"/api/recipes/{rid}").json()["rating"] == 3

def test_save_is_idempotent(client):
    rid = client.get("/api/recipes").json()["items"][0]["id"]
    assert client.post(f"/api/me/saved/{rid}").status_code == 201
    assert client.post(f"/api/me/saved/{rid}").status_code == 201
    assert len(client.get("/api/me/saved").json()) == 1

def test_non_admin_forbidden(client):
    assert client.get("/api/admin/users").status_code == 403

def test_logout_revokes(client):
    client.post("/api/auth/logout")
    assert client.get("/api/auth/me").status_code == 401
    