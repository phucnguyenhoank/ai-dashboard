from fastapi import APIRouter, Query, HTTPException
from app.schemas.detection import DetectionCreate, Detection
from app.core.database import detections_collection
from datetime import timedelta, datetime
from bson import ObjectId
from app.utils.image_storage import save_base64_image, get_base64_from_path
import os

router = APIRouter(prefix="/ai", tags=["detections"])


@router.post("/detections", response_model=Detection)
async def create_detection(detection: DetectionCreate):
    """
    Creates a new detection, but only if a similar detection (same camera and type)
    has not been logged in the last 5 seconds. This prevents duplicate events.
    """
    # Check for existing detection within the last 5 seconds
    existing = detections_collection.find_one({
        "user_id": detection.user_id,
        "camera_id": detection.camera_id,
        "type": detection.type,
        "timestamp": {
            "$gte": detection.timestamp - timedelta(seconds=5),
            "$lte": detection.timestamp
        }
    })

    if existing:
        # If a recent detection exists, we can't create a new one.
        # To avoid an error, we can return the existing one or a message.
        # Returning the existing one is often more useful.
        existing["id"] = str(existing["_id"])
        return Detection(**existing)

    # Save the image and get the path
    image_path = save_base64_image(detection.base64)
    if not image_path:
        raise HTTPException(status_code=500, detail="Failed to save image.")
    
    # Save the detection
    detection_dict = detection.model_dump(exclude={"base64"})
    detection_dict["image_path"] = image_path
    
    save_detection = detections_collection.insert_one(detection_dict)
    
    # After inserting, create the full response object
    response_detection = detection.model_dump()
    response_detection["id"] = str(save_detection["_id"])
    response_detection["image_path"] = image_path
    return Detection(**response_detection)


@router.get("/detections", response_model=list[Detection])
async def get_detections(
    user_id: str = Query(None),
    camera_id: str = Query(None),
    type: str = Query(None),
    seen: bool | None = Query(None, description="Filter by seen status (True/False), or None to ignore"),
    start_time: datetime = Query(None),
    end_time: datetime = Query(None),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    """
    Retrieves a list of detections with optional filters for user_id, camera_id, type,
    seen status, and time range. Supports pagination with skip and limit.
    """
    query = {}
    if user_id:
        query["user_id"] = user_id
    if camera_id:
        query["camera_id"] = camera_id
    if type:
        query["type"] = type
    if seen:
        query["seen"] = seen
    if start_time and end_time:
        query["timestamp"] = {"$gte": start_time, "$lte": end_time}
    elif start_time:
        query["timestamp"] = {"$gte": start_time}
    elif end_time:
        query["timestamp"] = {"$lte": end_time}

    detections = []
    cursor = detections_collection.find(query).sort("timestamp", -1).skip(skip).limit(limit)
    
    for doc in cursor:
        doc["id"] = str(doc["_id"])
        image_path = doc.get("image_path")
        if image_path and os.path.exists(image_path):
            doc["base64"] = get_base64_from_path(image_path)
        else:
            doc["base64"] = get_base64_from_path('images\loading_cat.png')
        detections.append(Detection(**doc))
        
    return detections


@router.delete("/detections/{detection_id}")
async def delete_detection(detection_id: str):
    try:
        doc = detections_collection.find_one({"_id": ObjectId(detection_id)})
        if doc:
            image_path = doc.get("image_path")
            if image_path and os.path.exists(image_path):
                os.remove(image_path)  # Delete the file
            detections_collection.delete_one({"_id": ObjectId(detection_id)})
            return {"message": "Detection deleted"}
        raise HTTPException(status_code=404, detail="Detection not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/detections")
async def delete_all_detections():
    try:
        docs = detections_collection.find({})  # Get all documents

        deleted_count = 0
        for doc in docs:
            image_path = doc.get("image_path")
            if image_path and os.path.exists(image_path):
                try:
                    os.remove(image_path)  # Delete the image file
                except Exception as e:
                    print(f"Error deleting file {image_path}: {e}")
            deleted_count += 1

        detections_collection.delete_many({})  # Remove all documents
        return {"message": f"Deleted {deleted_count} detections and their images"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


