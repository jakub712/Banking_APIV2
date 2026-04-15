import sys
sys.path.insert(0, './app')

from deps import engine, client, TestingSessionLocal
import pytest
from fastapi import status
from app.db.models import User
from sqlalchemy import text

@pytest.fixture
def test_user():
    user = User(
        username = 'test_user',
        first_name = 'test',
        last_name = 'user',
        hashed_password = 'password123',
        role = 'admin'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user 
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM User;"))
        connection.commit()

@pytest.fixture
def test_user2():
    user = User(
        username = 'test_user2',
        first_name = 'test',
        last_name = 'user',
        hashed_password = 'password1232',
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user 
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM User;"))
        connection.commit()


def test_create_user():
    response = client.post("/auth/create", json={
        "username": "new_user",
        "first_name": "new",
        "last_name": "user",
        "password": "password123",
        "role": "admin"
    })                           
    assert response.status_code == status.HTTP_201_CREATED

def test_create_admin(test_user2):
    responce = client.post("/auth/create_admin")
    assert responce.status_code == status.HTTP_200_OK

def test_promote_to_admin_invite(test_user, test_user2):
    response = client.post(f"/auth/promote/{test_user2.id}")
    assert response.status_code == status.HTTP_200_OK

def test_read_all_users(test_user):
    responce = client.get("/auth/all_users")
    assert responce.status_code == status.HTTP_200_OK

def test_read_all_transactions(test_user):
    responce = client.get("/auth/all_transactions")
    assert responce.status_code == status.HTTP_200_OK

def test_get_user(test_user, test_user2):
    responce = client.get(f"/auth/{test_user2.username}")
    assert responce.status_code == status.HTTP_200_OK
