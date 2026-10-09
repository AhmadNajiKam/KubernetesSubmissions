from fastapi import FastAPI

app = FastAPI()

app.state.counter: int = 0
@app.get("/pingpong")
async def pong():
    response = f"Pong {app.state.counter}"
    app.state.counter += 1
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=4000, log_level="error")

