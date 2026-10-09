import random
import string
import time
import threading
import sys
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse

def random_string(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# created ONCE on startup and stored in memory
RANDOM_STRING = random_string()
START_TIME = datetime.now()

app = FastAPI()

@app.get("/")
@app.get("/status")
def get_status():
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "random_string": RANDOM_STRING,
        "started_at": START_TIME.strftime("%Y-%m-%d %H:%M:%S")
    }

def log_loop():
    try:
        while True:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S: ')}{RANDOM_STRING}", flush=True)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nStopped.", file=sys.stderr)
        sys.exit(0)

# start logging thread when module loads
threading.Thread(target=log_loop, daemon=True).start()
