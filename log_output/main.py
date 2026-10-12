from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from datetime import datetime, timezone
import os
import uuid
import requests

app = FastAPI()

PING_PONG_URL = os.getenv(
    "PING_PONG_URL",
    "http://ping-pong-svc:2345/pings"
)

INFO_FILE_PATH = os.getenv(
    "INFO_FILE_PATH",
    "/app/shared/information.txt"
)

MESSAGE = os.getenv("MESSAGE", "")

RANDOM_STRING = str(uuid.uuid4())


def get_counter():
    response = requests.get(PING_PONG_URL, timeout=3)
    response.raise_for_status()
    return response.text.strip()


def get_file_content():
    with open(INFO_FILE_PATH, "r") as f:
        return f.read().strip()


@app.get("/")
@app.get("/status")
def get_status():
    counter = get_counter()
    file_content = get_file_content()
    timestamp = datetime.now(timezone.utc).isoformat(
        timespec="milliseconds"
    ).replace("+00:00", "Z")

    return PlainTextResponse(
        f"file content: {file_content}\n"
        f"env variable: MESSAGE={MESSAGE}\n"
        f"{timestamp}: {RANDOM_STRING}\n"
        f"Ping / Pongs: {counter}"
    )


@app.get("/raw")
def get_raw():
    return PlainTextResponse(get_counter())
