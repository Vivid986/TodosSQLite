from typing import Annotated

from fastapi import FastAPI, Depends, Path, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import Todos
from starlette import status
from request_models import TodoRequest

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# CREATE DB DEPENDENCY
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# get all todos
@app.get('/todos', status_code=status.HTTP_200_OK)
async def get_all_todos(db: db_dependency):
    todos = db.query(Todos).all()
    return  todos

# get single todo
@app.get('/todos/{todo_id}', status_code=status.HTTP_200_OK)
async def get_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo is not None:
        return todo

    raise HTTPException(status_code=404, detail='Todo not found.')

# create todo
@app.post('/todos', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    new_todo = Todos(**todo_request.model_dump())

    db.add(new_todo)
    db.commit()

# update
@app.put('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail='Todo not found.')

    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.priority = todo_request.priority
    todo.complete = todo_request.complete

    db.add(todo)
    db.commit()

# delete
@app.delete('/todos/{todo_id}')
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail='Todo not found.')

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

