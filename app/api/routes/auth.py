from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from app.db.models import User, Transaction
from app.db.session import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.schemas import auth
from app.api.routes.deps import db_dependency, get_db, user_dependancy
from app.schemas.auth import Token, CreateUserRequest
from dotenv import load_dotenv
import os

load_dotenv()

SECERET_KEY = os.getenv("SECERET_KEY")
ALGORITHM = os.getenv("ALGORITHM")  

router = APIRouter(prefix='/auth', tags = ['auth'])

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user( db:db_dependency, create_user_request:CreateUserRequest):
    user_model = User(
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        role = "user"
    )
    db.add(user_model)
    db.commit()

def authenticate_user(username:str, password:str, db):
    users = db.query(User).filter(User.username == username).first()
    if not users:
        return False
    if not bcrypt_context.verify(password, users.hashed_password):
        return False
    return users

def create_access_token(username:str, user_id:int, role: str, expires_delta:timedelta):
    encode = {'sub':username, 'id':user_id, 'role':role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECERET_KEY, algorithm=ALGORITHM)

    
@router.post("/token", include_in_schema=False, response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='wrong credentials')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return{'access_token':token, 'token_type':'bearer'}

@router.post("/create_admin",status_code=status.HTTP_200_OK)
async def create_admin(db:db_dependency, user:user_dependancy):
    admins =  db.query(User).filter(User.role == 'admin').count()
    if admins > 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='an admin already exsists')
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    
    user_model = db.query(User).filter(User.id == user['id']).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='user does not exsist')
    user_model.role = 'admin'
    db.commit()
    return {'messege':f'{user_model.username} has been promoted to admin'}

@router.post("/promote/{user_id}", status_code=status.HTTP_200_OK)
async def promote_to_admin_invite(db:db_dependency, user:user_dependancy, user_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    user_model = db.query(User).filter(User.id == user['id']).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='user does not exsist')
    if user_model.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='only an admin can promote others')

    user_model2 = db.query(User).filter(User.id == user_id).first()
    if user_model2 is None:
        raise HTTPException(status_code=404, detail='user does not exsist')
    user_model2.role = 'admin'
    db.commit()
    return {'messege':f'{user_model2.username} has been promoted to admin'}

@router.get("/all_users", status_code= status.HTTP_200_OK)
async def read_all_users(db:db_dependency, user:user_dependancy):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    user_model = db.query(User).filter(User.id == user['id']).first()
    if user_model.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='only an admin can access this data')
    all_users = db.query(User).all()
    return all_users

@router.get("/all_transactions", status_code=status.HTTP_200_OK)
async def read_all_transactions(db:db_dependency, user:user_dependancy):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    user_model = db.query(User).filter(User.id == user['id']).first()
    if user_model.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='only an admin can access this data')
    all_transactions = db.query(Transaction).all()
    return all_transactions

@router.get("/{user_name}", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependancy,db:db_dependency, user_name:str):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    user_m = db.query(User).filter(User.id == user['id']).first()
    if user_m.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='only an admin can access this data')
    
    user_model = db.query(User).filter(User.username == user_name).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='user not found')
    return {
        'id':user_model.id,
        'first_name':user_model.first_name,
        'last_name':user_model.last_name,
        'role':user_model.role
    }