from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.todo import Todo
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)


# ─── GET ALL TODOS (only current user's todos) ────────────
@router.get("/", response_model=List[TodoResponse])
def get_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    todos = db.query(Todo).filter(Todo.owner_id == current_user.id).all()
    return todos


# ─── GET ONE TODO ─────────────────────────────────────────
@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Make sure user owns this todo
    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return todo


# ─── CREATE TODO ──────────────────────────────────────────
@router.post("/", response_model=TodoResponse, status_code=201)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        owner_id=current_user.id  # automatically set to logged in user
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


# ─── UPDATE TODO ──────────────────────────────────────────
@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    updated_todo: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    # Update only fields that were sent
    if updated_todo.title is not None:
        todo.title = updated_todo.title
    if updated_todo.description is not None:
        todo.description = updated_todo.description
    if updated_todo.completed is not None:
        todo.completed = updated_todo.completed

    db.commit()
    db.refresh(todo)
    return todo


# ─── DELETE TODO ──────────────────────────────────────────
@router.delete("/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(todo)
    db.commit()
    return None