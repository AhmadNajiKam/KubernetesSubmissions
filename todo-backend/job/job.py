import os
import requests
import psycopg
from urllib.parse import urljoin

DATABASE_URL = os.environ["DATABASE_URL"]
MAX_TODO_LENGTH = int(os.environ.get("MAX_TODO_LENGTH", "140"))

HEADERS = {
    "User-Agent": f"TodoReminderBot/1.0 (ahmadnajikam@gmail.com)"
}


def main():
    for _ in range(10):
        response = requests.get(
            "https://en.wikipedia.org/wiki/Special:Random",
            headers=HEADERS,
            allow_redirects=False,
            timeout=10,
        )
        response.raise_for_status()

        url = urljoin(
            response.url,
            response.headers["Location"],
        )

        todo = f"Read {url}"

        if len(todo) <= MAX_TODO_LENGTH:
            with psycopg.connect(DATABASE_URL) as conn:
                conn.execute(
                    "INSERT INTO todos (text) VALUES (%s)",
                    (todo,),
                )

            print(f"Created todo: {todo}")
            return

    raise RuntimeError("Could not find an article within the length limit")


if __name__ == "__main__":
    main()
