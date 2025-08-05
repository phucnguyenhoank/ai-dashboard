from fastapi import FastAPI
from app.api.endpoints import detections

app = FastAPI(title="AI Dashboard Backend")

app.include_router(detections.router)

@app.get("/")
async def root():
    return {"message": "Welcome to AI Dashboard Backend!"}