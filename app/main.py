# app/main.py
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, task
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()  # .env を読み込む

JWT_SECRET = os.getenv("JWT_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# モデルに基づいてテーブルを作成
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(task.router)

@app.get("/")
def read_root():
    return {"message": "Hello, Todo App!"}
