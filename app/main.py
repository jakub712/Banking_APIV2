from fastapi import FastAPI
from app.db.session import engine
from app.db import models
from app.api.routes import accounts, auth, transfers
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def serve_frontend():
    return FileResponse("frontend.html")

models.Base.metadata.create_all(bind=engine)


app.include_router(accounts.router)
app.include_router(transfers.router)
app.include_router(auth.router)