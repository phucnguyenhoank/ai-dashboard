from fastapi import APIRouter
from app.schemas.detection import DetectionCreate, Detection
from app.core.database import detections_collection

router = APIRouter(prefix="/ai", tags=["detections"])

@router.post("/detections", response_model=Detection)
async def create_detection(detection: DetectionCreate):
    # Convert Pydantic model to dict and insert into MongoDB
    detection_dict = detection.model_dump()
    result = detections_collection.insert_one(detection_dict)
    # Return the inserted detection with its MongoDB _id
    return {"id": str(result.inserted_id), **detection_dict}

@router.get("/detections", response_model=list[Detection])
async def get_detections():
    detections = []
    for doc in detections_collection.find():
        doc["id"] = str(doc["_id"])  # Convert ObjectId to string
        del doc["_id"]  # Remove MongoDB's _id field
        detections.append(Detection(**doc))
    return detections