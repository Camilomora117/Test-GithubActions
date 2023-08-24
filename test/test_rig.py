import pytest
from fastapi.testclient import TestClient
from fastapi import status
from main import app
from schemas.user import UserSingUp
from config.database import Session
from services.user import UserService
from utils.jwt_manager import create_token

credentials = {"username": "prueba", "password": "prueba", "email": "prueba@gmail.com", "company_id": "1"}

rig = {
  "name": "testrig",
  "company_id": 1,
  "user_id": 1
}

id_rig_global = 0

def get_token():
    token = create_token(credentials)
    return token

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client
    db = Session()
    UserService(db).delete_user_by_email("prueba@gmail.com")

@pytest.fixture(scope="module")
def test_user():
    return credentials

@pytest.fixture(scope="module")
def test_rig():
    return rig

def test_create_test_for_tests(test_client, test_user):
    test_client.post("/signup", json=test_user)

def test_update_rig_not_found(test_client, test_rig):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.put("/rigs/1000", headers=headers, json=test_rig)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Rig not found"}

def test_create_rig_successfully(test_client, test_rig):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.post("/rigs", json=test_rig,headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"message": "Rig Created"}

def test_get_rigs_status_code(test_client):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.get("/rigs", headers=headers)
    global id_rig_global
    id_rig_global = int(response.json()[-1]['id'])
    assert response.status_code == status.HTTP_200_OK

def test_update_rig_successfully(test_client, test_rig):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.put("/rigs/" + str(id_rig_global), headers=headers, json=test_rig)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Modified rig"}
    
def test_get_rig_by_id_not_found(test_client):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.get("/rigs/1000", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Rig not found"}

def test_delete_rig_successfully(test_client):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.delete("/rigs/" + str(id_rig_global), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Deleted rig"}

def test_delete_rig_not_found(test_client):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.delete("/rigs/1000", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Rig not found"}