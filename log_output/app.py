import random
import string
import time
import sys
from datetime import datetime

def random_string(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

if __name__ == "__main__":
    try:
        while True:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S: "), end="")
            print(random_string(), flush=True)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nStopped.", file=sys.stderr)
        sys.exit(0)
