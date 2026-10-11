import os
import time
from html import escape
from pathlib import Path
from threading import Lock

import requests
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response

app = FastAPI()

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://todo-backend-svc:2345",
).rstrip("/")

CACHE_DIR = Path(os.getenv("CACHE_DIR", "./cache"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_PATH = CACHE_DIR / "image.jpg"
CACHE_SECONDS = 600
image_lock = Lock()


@app.get("/image")
def get_image():
    with image_lock:
        expired = (
            not IMAGE_PATH.exists()
            or time.time() - IMAGE_PATH.stat().st_mtime >= CACHE_SECONDS
        )

        if expired:
            try:
                response = requests.get(
                    "https://picsum.photos/1200",
                    timeout=20,
                )
                response.raise_for_status()

                # Replace the old image only after a successful download.
                temporary_path = CACHE_DIR / "image.tmp"
                temporary_path.write_bytes(response.content)
                temporary_path.replace(IMAGE_PATH)

            except requests.RequestException:
                if not IMAGE_PATH.exists():
                    raise HTTPException(
                        status_code=502,
                        detail="Could not download image",
                    )

        image = IMAGE_PATH.read_bytes()

    return Response(
        content=image,
        media_type="image/jpeg",
        headers={"Cache-Control": "no-store"},
    )


@app.get("/", response_class=HTMLResponse)
def index():
    try:
        response = requests.get(
            f"{BACKEND_URL}/todos",
            timeout=5,
        )
        response.raise_for_status()
        todos = response.json()

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Todo backend is unavailable",
        )

    items = "".join(
        f"<li>{escape(todo['text'])}</li>"
        for todo in todos
    )

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Todo App</title>

        <style>
            body {{
                max-width: 600px;
                margin: 40px auto;
                padding: 0 16px;
                font-family: Arial, sans-serif;
            }}

            img {{
                width: 100%;
                border-radius: 8px;
            }}

            form {{
                display: flex;
                gap: 8px;
                margin: 20px 0;
            }}

            input {{
                flex: 1;
                min-width: 0;
                padding: 10px;
            }}

            button {{
                padding: 10px 16px;
                cursor: pointer;
            }}

            li {{
                margin-bottom: 10px;
                overflow-wrap: anywhere;
            }}
        </style>
    </head>

    <body>
        <h1>Todo App</h1>

        <img src="/image" alt="Random cached photograph">

        <form action="/todos" method="post">
            <input
                type="text"
                name="text"
                placeholder="Write a todo"
                maxlength="140"
                required
            >
            <button type="submit">Send</button>
        </form>

        <ul>
            {items or "<li>No todos yet.</li>"}
        </ul>
    </body>
    </html>
    """


@app.post("/todos")
def submit_todo(text: str = Form(...)):
    text = text.strip()

    if not text or len(text) > 140:
        raise HTTPException(
            status_code=422,
            detail="Todo must contain between 1 and 140 characters",
        )

    try:
        response = requests.post(
            f"{BACKEND_URL}/todos",
            json={"text": text},
            timeout=5,
        )
        response.raise_for_status()

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Could not save todo",
        )

    return RedirectResponse(url="/", status_code=303)
