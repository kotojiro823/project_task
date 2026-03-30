# app/main.py
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, task, user
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# .env を読み込む（Renderでは不要だが、ローカル用に残す）
load_dotenv()

# 環境変数の読み込み（必要に応じて使用）
JWT_SECRET = os.getenv("JWT_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

# 許可するオリジン（フロントエンドのURL） 
origins = [ 
    "http://localhost:3000",  # ローカル開発用
    "https://todo-frontend-mjuw.onrender.com",  # 本番用
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# モデルに基づいてテーブルを作成（存在しない場合のみ）
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# ルーターの登録
app.include_router(auth.router)
app.include_router(task.router)
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "Hello, Todo App!"}

# 静的ファイルのマウント
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# favicon.ico のルートを追加
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("app/static/favicon.ico")
