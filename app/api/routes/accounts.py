from fastapi import APIRouter, HTTPException
from app.db.models import User, Account
from starlette import status
from app.api.routes.deps import db_dependency, user_dependancy

router = APIRouter(prefix='/accounts', tags=['accounts'])

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_account(user:user_dependancy, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    user_model = db.query(User).filter(user['id'] == User.id).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    account = Account(
        user_id = user["id"],
        balance_pence = 0,
        account_type = "current"
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return{
        'account_id': account.id,
        'user_id':account.user_id,
        'balance': account.balance_pence,
        'account_type': account.account_type
    }

@router.get("/get_user", status_code=status.HTTP_200_OK)
def get_user_details(user:user_dependancy, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    user_model = db.query(User).filter(user['id'] == User.id).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    account = db.query(Account).filter(Account.user_id == user['id']).first()
    if account is None:
        raise HTTPException(status_code=404, detail='account not found')
    return{
        'account_id':account.id,
        'user_id':account.user_id,
        'balance':account.balance_pence,
    }