import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.main import app
from app.api.routes.deps import get_db, get_current_user
from app.db.session import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def overide_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'testuser', 'id': 1, 'user_role': 'admin'}

def override_get_current_user_2():
    return {'username': 'testuser2', 'id': 2, 'user_role': 'user'}

app.dependency_overrides[get_db] = overide_get_db
app.dependency_overrides[get_current_user] = override_get_current_user
client = TestClient(app)
