import sys
sys.path.insert(0, './app')

from deps import engine, client, TestingSessionLocal
import pytest
from fastapi import status
from db.models import User, Account
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
def test_user_account():
    account = Account(
        user_id = 1,
        balance_pence = 0,
        account_type = "current"
    )

    db = TestingSessionLocal()
    db.add(account)
    db.commit()
    yield account 
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM Account;"))
        connection.commit()

def test_create_account(test_user):
    response = client.post("/accounts/create", json={
        "user_id": "1",
        "balance_pence": 0,
        "account_type":"current"
    })                           
    assert response.status_code == status.HTTP_201_CREATED

def test_get_user_details(test_user, test_user_account):
    response = client.get("/accounts/get_user")
    assert response.status_code == 200
