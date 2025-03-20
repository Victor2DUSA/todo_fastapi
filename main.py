from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, SQLModel, create_engine, select
from models import Todo, TodoCreate, TodoGet, TodoUpdate

from db import create_db_and_tables, SessionDep


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/todos/", response_model=TodoGet)
def create_todo(todo: TodoCreate, session: SessionDep):
    db_todo = Todo.model_validate(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.get("/todos/", response_model=list[TodoGet])
def read_todoes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    Todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
    return Todos


@app.get("/todos/{hero_id}", response_model=TodoGet)
def read_todo(hero_id: int, session: SessionDep):
    hero = session.get(Todo, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return Todo


@app.patch("/todos/{hero_id}", response_model=TodoGet)
def update_todo(hero_id: int, hero: TodoUpdate, session: SessionDep):
    todo_db = session.get(Todo, hero_id)
    if not todo_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    todo_data = hero.model_dump(exclude_unset=True)
    todo_db.sqlmodel_update(todo_data)
    session.add(todo_db)
    session.commit()
    session.refresh(todo_db)
    return todo_db


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, session: SessionDep):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(todo)
    session.commit()
    return {"ok": True}