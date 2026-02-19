# app/routers/task.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.deps import get_current_user_id
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatusUpdate
from app.services.task_service import (
    create_task, get_tasks, update_task, delete_task, update_task_status, toggle_task_status
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse)
def create(data: TaskCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return create_task(db, user_id, data)

@router.get("/", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return get_tasks(db, user_id)

@router.put("/{task_id}", response_model=TaskResponse)
def update(task_id: int, data: TaskUpdate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    task = update_task(db, task_id, data, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}")
def delete(task_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    ok = delete_task(db, task_id, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}

@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_status(task_id: int, data: TaskStatusUpdate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    task = update_task_status(db, task_id, data.completed, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/{task_id}/toggle", response_model=TaskResponse)
def toggle_status(task_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    task = toggle_task_status(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
