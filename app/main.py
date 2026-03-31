from fastapi import FastAPI
from app.db.session import engine, SessionLocal, Base
from app.db.models import User, Account, Transaction
from app.db import models
from app.api.routes import accounts, auth, transfers

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(accounts.router)
app.include_router(transfers.router)
app.include_router(auth.router)