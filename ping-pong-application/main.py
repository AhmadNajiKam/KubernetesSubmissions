import os
import psycopg
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

DATABASE_URL = os.environ["DATABASE_URL"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS counter (
                id INT PRIMARY KEY,
                value BIGINT NOT NULL DEFAULT 0
            )
        """)
        conn.execute("""
            INSERT INTO counter (id, value)
            VALUES (1, 0)
            ON CONFLICT (id) DO NOTHING
        """)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/pingpong")
def pong():
    with psycopg.connect(DATABASE_URL) as conn:
        result = conn.execute("""
            UPDATE counter
            SET value = value + 1
            WHERE id = 1
            RETURNING value - 1
        """)
        count = result.fetchone()[0]

    return PlainTextResponse(f"Pong {count}")


@app.get("/pings")
def get_pings():
    with psycopg.connect(DATABASE_URL) as conn:
        result = conn.execute("SELECT value FROM counter WHERE id = 1")
        count = result.fetchone()[0]

    return PlainTextResponse(str(count))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4000, log_level="error")
