from fastapi import FastAPI

app = FastAPI(title="FlashCards API")

@app.get("/api/health")
async def health():
    return {"status": "ok"}
