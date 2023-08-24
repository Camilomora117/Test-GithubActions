import pytest
from fastapi.testclient import TestClient
from fastapi import status
from main import app
from schemas.user import UserSingUp
from config.database import Session
from services.user import UserService
from utils.jwt_manager import create_token

credentials = {"username": "prueba", "password": "prueba", "email": "prueba@gmail.com", "company_id": "1"}

company  = {
  "name": "TestEmpresa",
  "description": "Descripcion empresa test",
  "email": "test@test.com",
  "phone": 32038231
}

id_company_global = 0

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
def test_company():
    return company

def test_create_test_for_tests(test_client, test_user):
    test_client.post("/signup", json=test_user)

def test_update_company_not_found(test_client, test_company):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.put("/companies/1000", headers=headers, json=test_company)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Company not found"}

def test_create_company_successfully(test_client, test_company):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.post("/companies", json=test_company,headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"message": "Company Created"}

def test_get_companies_status_code(test_client):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.get("/companies", headers=headers)
    global id_company_global
    id_company_global = int(response.json()[-1]['id'])
    assert response.status_code == status.HTTP_200_OK

def test_update_rig_successfully(test_client, test_company):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.put("/companies/" + str(id_company_global), headers=headers, json=test_company)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Modified company"}

def test_get_company_by_id_not_found(test_client):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.get("/companies/1000", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Company not found"}

def test_delete_company_successfully(test_client):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.delete("/companies/" + str(id_company_global), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Deleted company"}

def test_delete_company_not_found(test_client):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = test_client.delete("/companies/1000", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Company not found"}