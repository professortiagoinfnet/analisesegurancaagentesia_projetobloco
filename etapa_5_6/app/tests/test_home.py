from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "ok"
    }

def test_login_valido():

    response = client.post(
        "/token",
        data={
            "username": "admin",
            "password": "admin"
        }
    )

    assert response.status_code == 200

def test_login_invalido():

    response = client.post(
        "/token",
        data={
            "username": "admin",
            "password": "senha_errada"
        }
    )

    assert response.status_code == 401

def test_rota_protegida_sem_token():

    response = client.get(
        "/predictions/1"
    )

    assert response.status_code == 401

