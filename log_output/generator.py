import random
import string
import time
from datetime import datetime
import os

def random_string(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

RANDOM_STRING = random_string()
START_TIME = datetime.now()
FILE_PATH = "/app/shared/log.txt"


os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

print(f"Generated on startup: {RANDOM_STRING} at {START_TIME}")

while True:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp}: {RANDOM_STRING}\n"
    
    with open(FILE_PATH, "a") as f:
        f.write(line)
    
    print(line, end='')
    time.sleep(5)
