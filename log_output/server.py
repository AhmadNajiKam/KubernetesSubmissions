from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import os

FILE_PATH = "/app/shared/log.txt"

app = FastAPI()

@app.get("/")
@app.get("/status")
def get_status():
    if not os.path.exists(FILE_PATH):
        return JSONResponse({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "content": [],
            "message": "File not created yet"
        })

    with open(FILE_PATH, "r") as f:
        lines = f.read().strip().split("\n")

    # parse last line to get the random_string and started_at
    last_random = lines[-1].split(": ")[-1] if lines else None
    
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "random_string": last_random,
        "file_content": lines,
        "total_lines": len(lines)
    }

@app.get("/raw")
def get_raw():
    if not os.path.exists(FILE_PATH):
        return "File empty"
    with open(FILE_PATH, "r") as f:
        return f.read()
