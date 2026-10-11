from fastapi import FastAPI
import os

app: FastAPI = FastAPI()
FILE_PATH: str = "/app/shared/counter.txt"

os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

# Restore counter after restart
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r") as f:
        app.state.counter = int(f.read().strip())
else:
    app.state.counter = 0

@app.get("/pingpong")
async def pong():
    response = f"Pong {app.state.counter}"
    app.state.counter += 1

    with open(FILE_PATH, "w") as f:
        f.write(str(app.state.counter))

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4000, log_level="error")
