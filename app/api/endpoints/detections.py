from fastapi import APIRouter, Query
from app.schemas.detection import DetectionCreate, Detection
from app.core.database import detections_collection
from datetime import timedelta
from datetime import datetime

router = APIRouter(prefix="/ai", tags=["detections"])

@router.post("/detections", response_model=Detection)
async def create_detection(detection: DetectionCreate):
    # Check for existing detection within the last 5 seconds
    existing = detections_collection.find_one({
        "camera_id": detection.camera_id,
        "type": detection.type,
        "timestamp": {
            "$gte": detection.timestamp - timedelta(seconds=5),
            "$lte": detection.timestamp
        }
    })
    if existing:
        return {"message": "Detection already exists within 5 seconds"}
    else:
        detection_dict = detection.model_dump()
        result = detections_collection.insert_one(detection_dict)
        return {"id": str(result.inserted_id), **detection_dict}

@router.get("/detections", response_model=list[Detection])
async def get_detections(
    camera_id: str = Query(None),
    type: str = Query(None),
    start_time: datetime = Query(None),
    end_time: datetime = Query(None),
    skip: int = 0,
    limit: int = 100
):
    query = {}
    if camera_id:
        query["camera_id"] = camera_id
    if type:
        query["type"] = type
    if start_time and end_time:
        query["timestamp"] = {"$gte": start_time, "$lte": end_time}
    elif start_time:
        query["timestamp"] = {"$gte": start_time}
    elif end_time:
        query["timestamp"] = {"$lte": end_time}
    # Might change seen to true if needed
    # seen = False
    detections = []
    for doc in detections_collection.find(query).sort("timestamp", -1).skip(skip).limit(limit):
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        detections.append(Detection(**doc))
    return detections