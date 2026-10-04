import os
from fastapi import FastAPI

app = FastAPI()

PORT = int(os.getenv("PORT", "3000"))

@app.get("/")
def root():
    return {"message": "Todo app is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# For local run
if __name__ == "__main__":
    import uvicorn
    print(f"Server started in port {PORT}", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=PORT)
