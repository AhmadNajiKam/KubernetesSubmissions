import os
import time
from html import escape
from pathlib import Path
from threading import Lock

import requests
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response

app = FastAPI()

# Configuration from environment variables
BACKEND_URL = os.environ["BACKEND_URL"].rstrip("/")
IMAGE_SOURCE_URL = os.environ["IMAGE_SOURCE_URL"]

CACHE_DIR = Path(os.environ["CACHE_DIR"])
CACHE_FILENAME = os.environ["CACHE_FILENAME"]
CACHE_SECONDS = int(os.environ["CACHE_SECONDS"])

IMAGE_REQUEST_TIMEOUT = float(os.environ["IMAGE_REQUEST_TIMEOUT"])
BACKEND_REQUEST_TIMEOUT = float(os.environ["BACKEND_REQUEST_TIMEOUT"])

MAX_TODO_LENGTH = int(os.environ["MAX_TODO_LENGTH"])
IMAGE_MEDIA_TYPE = os.environ["IMAGE_MEDIA_TYPE"]

CACHE_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_PATH = CACHE_DIR / CACHE_FILENAME
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
                    IMAGE_SOURCE_URL,
                    timeout=IMAGE_REQUEST_TIMEOUT,
                )
                response.raise_for_status()

                temporary_path = IMAGE_PATH.with_name(
                    IMAGE_PATH.name + ".tmp"
                )

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
        media_type=IMAGE_MEDIA_TYPE,
        headers={"Cache-Control": "no-store"},
    )


@app.get("/", response_class=HTMLResponse)
def index():
    try:
        response = requests.get(
            f"{BACKEND_URL}/todos",
            timeout=BACKEND_REQUEST_TIMEOUT,
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
                maxlength="{MAX_TODO_LENGTH}"
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

    if not text or len(text) > MAX_TODO_LENGTH:
        raise HTTPException(
            status_code=422,
            detail=f"Todo must contain between 1 and {MAX_TODO_LENGTH} characters",
        )

    try:
        response = requests.post(
            f"{BACKEND_URL}/todos",
            json={"text": text},
            timeout=BACKEND_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Could not save todo",
        )

    return RedirectResponse(url="/", status_code=303)

