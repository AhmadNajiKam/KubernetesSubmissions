import os
import psycopg
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Configuration from environment variables
MAX_TODO_LENGTH = int(os.environ["MAX_TODO_LENGTH"])
DATABASE_URL = os.environ["DATABASE_URL"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                text TEXT NOT NULL
            )
        """)
    yield


app = FastAPI(lifespan=lifespan)


class TodoCreate(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=MAX_TODO_LENGTH,
    )


@app.get("/todos")
def get_todos():
    with psycopg.connect(DATABASE_URL) as conn:
        result = conn.execute("""
            SELECT id, text FROM todos ORDER BY id
        """)
        return [
            {"id": row[0], "text": row[1]}
            for row in result.fetchall()
        ]


@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate):
    text = todo.text.strip()

    if not text:
        raise HTTPException(
            status_code=422,
            detail="Todo cannot be empty",
        )

    with psycopg.connect(DATABASE_URL) as conn:
        result = conn.execute(
            """
            INSERT INTO todos (text)
            VALUES (%s)
            RETURNING id, text
            """,
            (text,),
        )
        row = result.fetchone()

    return {
        "id": row[0],
        "text": row[1],
    }
