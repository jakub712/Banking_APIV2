from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from db.session import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from starlette import status
from dotenv import load_dotenv
import os
load_dotenv()

SECERET_KEY = os.getenv("SECERET_KEY")
ALGORITHM = os.getenv("ALGORITHM")  

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
def get_current_user(token:Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECERET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        user_id:int = payload.get('id')
        user_role:str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='wrong credentials')
        return{'username':username, 'id':user_id, 'user_role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='wrong credentials')
    
user_dependancy = Annotated[dict, Depends(get_current_user)]
