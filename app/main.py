from fastapi import FastAPI
from db.session import engine
from db import models
from api.routes import accounts, auth, transfers

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(accounts.router)
app.include_router(transfers.router)
app.include_router(auth.router)