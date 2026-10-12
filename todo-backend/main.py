import os
from threading import Lock

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# Configuration from environment variables
MAX_TODO_LENGTH = int(os.environ["MAX_TODO_LENGTH"])

todos = []
lock = Lock()


class TodoCreate(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=MAX_TODO_LENGTH,
    )


@app.get("/todos")
def get_todos():
    with lock:
        return list(todos)


@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate):
    text = todo.text.strip()

    if not text:
        raise HTTPException(
            status_code=422,
            detail="Todo cannot be empty",
        )

    with lock:
        new_todo = {
            "id": len(todos) + 1,
            "text": text,
        }
        todos.append(new_todo)

    return new_todo
