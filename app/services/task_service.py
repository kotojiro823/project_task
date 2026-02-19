# app/services/task_service.py
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

def create_task(db: Session, user_id: int, data: TaskCreate):
    task = Task(user_id=user_id, title=data.title, description=data.description)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db: Session, user_id: int):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return [TaskResponse.from_orm(task) for task in tasks]


def update_task(db: Session, task_id: int, data: TaskUpdate, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        return None

    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.completed is not None:
        task.completed = data.completed

    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        return False

    db.delete(task)
    db.commit()
    return True

def update_task_status(db: Session, task_id: int, completed: bool, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        return None

    task.completed = completed
    db.commit()
    db.refresh(task)
    return task

def toggle_task_status(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        return None

    task.completed = not task.completed
    db.commit()
    db.refresh(task)
    return task
