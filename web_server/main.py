import os
import time
import fcntl
import tempfile
import logging
from pathlib import Path

import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

CACHE_DIR = Path(
    os.getenv("IMAGE_CACHE_DIR", str(BASE_DIR / "data"))
)
CACHE_TTL = int(os.getenv("IMAGE_CACHE_TTL_SECONDS", "600"))

IMAGE_PATH = CACHE_DIR / "picture.jpg"
LOCK_PATH = CACHE_DIR / "picture.lock"

CACHE_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "templates" / "index.html")


def cache_expired():
    if not IMAGE_PATH.exists():
        return True

    age = time.time() - IMAGE_PATH.stat().st_mtime
    return age >= CACHE_TTL


def download_image():
    url = f"https://picsum.photos/1200/800.jpg?random={time.time_ns()}"

    fd, temp_path = tempfile.mkstemp(dir=CACHE_DIR)

    try:
        with os.fdopen(fd, "wb") as file:
            with requests.get(
                url, stream=True, timeout=(5, 30)
            ) as response:
                response.raise_for_status()

                if not response.headers.get(
                    "Content-Type", ""
                ).lower().startswith("image/jpeg"):
                    raise ValueError("Expected a JPEG image")

                for chunk in response.iter_content(65536):
                    if chunk:
                        file.write(chunk)

            file.flush()
            os.fsync(file.fileno())

        if os.path.getsize(temp_path) == 0:
            raise ValueError("Downloaded image is empty")

        os.utime(temp_path, None)
        os.replace(temp_path, IMAGE_PATH)

    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@app.get("/image")
def get_image():
    if cache_expired():
        with LOCK_PATH.open("a+") as lock_file:
            fcntl.flock(lock_file, fcntl.LOCK_EX)

            # Recheck in case another request refreshed it.
            if cache_expired():
                try:
                    download_image()
                except (requests.RequestException, OSError, ValueError):
                    logger.exception("Image download failed")

                    # Use the stale image if available.
                    if not IMAGE_PATH.exists():
                        raise HTTPException(
                            status_code=503,
                            detail="Image unavailable",
                        )

    return FileResponse(
        IMAGE_PATH,
        media_type="image/jpeg",
        headers={"Cache-Control": "no-store"},
    )
