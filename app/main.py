from fastapi import FastAPI
from app.api.endpoints import ai_output

app = FastAPI(title="AI Dashboard Backend")

# Include API routes
app.include_router(ai_output.router)

@app.get("/")
async def root():
    return {"message": "Welcome to AI Dashboard Backend!"}