from fastapi import APIRouter, HTTPException, Query
from app.schemas.camera import CameraCreate, Camera, CameraWithStats, CameraSummary
from app.core.database import cameras_collection, detections_collection
from app.utils.image_storage import save_base64_image, get_base64_from_path
from bson import ObjectId
import os

router = APIRouter(prefix="/ai", tags=["cameras"])

@router.post("/cameras", response_model=Camera)
async def create_camera(camera: CameraCreate):
    """
    Creates a new camera, saving its image to disk and storing the path in the database.
    """
    # Check if camera_id already exists
    if cameras_collection.find_one({"camera_id": camera.camera_id}):
        raise HTTPException(status_code=400, detail=f"Camera with camera_id {camera.camera_id} already exists")

    # Save the image to disk if provided
    image_path = None
    if camera.base64:
        image_path = save_base64_image(camera.base64)
        if image_path is None:
            raise HTTPException(status_code=400, detail="Invalid base64 image")

    # Prepare camera data for database (exclude base64, include image_path)
    camera_dict = camera.model_dump(exclude={"base64"})
    camera_dict["image_path"] = image_path

    # Insert into MongoDB
    result = cameras_collection.insert_one(camera_dict)

    # Prepare response with original base64 and image_path
    response_dict = camera.model_dump()
    response_dict["id"] = str(result.inserted_id)
    response_dict["image_path"] = image_path
    return Camera(**response_dict)

@router.get("/cameras", response_model=list[CameraWithStats])
async def get_cameras(
    camera_id: str = Query(None, description="Filter by camera_id"),
    name: str = Query(None, description="Filter cameras whose name contains this text"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    """
    Retrieves a list of cameras with optional camera_id filter and pagination.
    """
    query = {}
    if camera_id:
        query["camera_id"] = camera_id
    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    cameras = []
    cursor = cameras_collection.find(query).skip(skip).limit(limit)
    
    for doc in cursor:
        doc["id"] = str(doc["_id"])
        image_path = doc.get("image_path")
        if image_path and os.path.exists(image_path):
            doc["base64"] = get_base64_from_path(image_path)
        else:
            doc["base64"] = None
        
        unread_count = detections_collection.count_documents({
            "camera_id": doc["camera_id"],
            "seen": False
        })
        doc["unread_detections"] = unread_count
        cameras.append(CameraWithStats(**doc))
        
    return cameras


@router.get("/cameras/summary", response_model=CameraSummary)
async def get_user_summary():
    """
    Returns total number of users and number of active users.
    """
    total = cameras_collection.count_documents({})
    active = total # cameras_collection.count_documents({"is_active": True})

    return CameraSummary(
        total_cameras=total,
        active_cameras=active
    )


@router.delete("/cameras")
async def delete_all_detections():
    try:
        docs = cameras_collection.find({})  # Get all documents

        deleted_count = 0
        for doc in docs:
            image_path = doc.get("image_path")
            if image_path and os.path.exists(image_path):
                try:
                    os.remove(image_path)  # Delete the image file
                except Exception as e:
                    print(f"Error deleting file {image_path}: {e}")
            deleted_count += 1

        cameras_collection.delete_many({})  # Remove all documents
        return {"message": f"Deleted {deleted_count} cameras and their images"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
