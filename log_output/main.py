from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import os

COUNTER_PATH = "/app/shared/counter.txt"

app = FastAPI()

@app.get("/")
@app.get("/status")
def get_status():
    if not os.path.exists(COUNTER_PATH):
        return PlainTextResponse("Ping / Pongs: 0")

    with open(COUNTER_PATH, "r") as f:
        counter = f.read().strip()

    return PlainTextResponse(f"Ping / Pongs: {counter}")

@app.get("/raw")
def get_raw():
    if not os.path.exists(COUNTER_PATH):
        return "File empty"

    with open(COUNTER_PATH, "r") as f:
        return f.read()
