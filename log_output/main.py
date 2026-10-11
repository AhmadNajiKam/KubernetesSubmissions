from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import os
import requests

app = FastAPI()

PING_PONG_URL = os.getenv(
    "PING_PONG_URL",
    "http://ping-pong-svc:2345/pings"
)


def get_counter():
    response = requests.get(PING_PONG_URL, timeout=3)
    response.raise_for_status()
    return response.text.strip()


@app.get("/")
@app.get("/status")
def get_status():
    counter = get_counter()
    return PlainTextResponse(f"Ping / Pongs: {counter}")


@app.get("/raw")
def get_raw():
    return PlainTextResponse(get_counter())
