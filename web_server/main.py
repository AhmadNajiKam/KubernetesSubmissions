import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from string import ascii_letters, digits
from random import choice

app = FastAPI()

PORT = int(os.getenv("PORT", "3000"))
def random_str(length:int = 12) -> str:
    chars: str = ascii_letters + digits
    return "".join(choice(chars) for _ in range(length))

app_name: str = random_str(12)
@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <html>
        <head>
            <title>{app_name}</title>
        </head>
        <body>
            <h6>{app_name} : {random_str(10)}</h6>
        </body>
    </html>
    """

@app.get("/health")
def health():
    return {"status": "ok"}

# For local run
if __name__ == "__main__":
    import uvicorn
    print(f"Server started with {app_name}", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=PORT)
