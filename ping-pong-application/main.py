from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()
app.state.counter = 0


@app.get("/pingpong")
async def pong():
    response = f"Pong {app.state.counter}"
    app.state.counter += 1
    return PlainTextResponse(response)


@app.get("/pings")
async def get_pings():
    return PlainTextResponse(str(app.state.counter))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4000, log_level="error")
