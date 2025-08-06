from fastapi import FastAPI
from app.api.endpoints import detections
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Dashboard Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc chỉ origin cụ thể như: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detections.router)

@app.get("/")
async def root():
    return {"message": "Welcome to AI Dashboard Backend!"}