import sys
sys.path.insert(0, './app')

from deps import engine, client, TestingSessionLocal
import pytest
from fastapi import status
from db.models import User,Transaction, Account
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
        balance_pence = 100000000,
        account_type = "current"
    )

    db = TestingSessionLocal()
    db.add(account)
    db.commit()
    yield account 
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM Account;"))
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

@pytest.fixture
def test_user_account2():
    account = Account(
        user_id = 2,
        balance_pence = 100000,
        account_type = "current"
    )

    db = TestingSessionLocal()
    db.add(account)
    db.commit()
    yield account 
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM Account;"))
        connection.commit()

def test_deposit_money(test_user, test_user_account):
    responce = client.post("/transactions/deposit", json={
        "from_account_id" : "None",
        "to_account_id" : test_user_account.id,
        "amount_pence" : 5000,
        "status" : "Completed",
        "user_id" : 1    
    })
    assert responce.status_code == status.HTTP_200_OK

def test_withdraw_money(test_user, test_user_account):
    responce = client.post("/transactions/withdraw", json={
        "from_account_id" : 1,
        "to_account_id" : None,
        "amount_pence" : 500,
        "status" : "Completed",
        "user_id" : 1
    })
    assert responce.status_code == status.HTTP_200_OK

def test_transfer_money(test_user, test_user_account, test_user2, test_user_account2):
    responce = client.post(f"/transactions/transfer/{test_user_account2.id}", json={
        "from_account_id": test_user_account.id,
        "to_account_id": test_user_account2.id,
        "amount_pence": 500
    })
    assert responce.status_code == status.HTTP_200_OK

def test_all_transactions_for_user(test_user, test_user_account):
    responce = client.get("/transactions/all")
    assert responce.status_code == status.HTTP_200_OK
