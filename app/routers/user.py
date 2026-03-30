# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    password = data.get("password")

    if password != "delete":
        raise HTTPException(status_code=403, detail="パスワードが正しくありません")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    db.delete(user)
    db.commit()
    return

