from fastapi import APIRouter
from app.schemas.ai_output import AIOutputCreate, AIOutput

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/output", response_model=AIOutputCreate)
async def receive_ai_output(ai_output: AIOutput):
    # For now, just return the received data
    # Later, you can save it to a database or process it
    return {"id": 1, "model_name": ai_output.model_name, "output": ai_output.output}