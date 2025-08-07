from fastapi import APIRouter, HTTPException, Query
from app.schemas.user import UserCreate, User, UserSummary
from app.core.database import users_collection
from bson import ObjectId
import os

router = APIRouter(prefix="/ai", tags=["users"])

@router.post("/users", response_model=User)
async def create_user(user: UserCreate):
    """
    Creates a new user.
    """
    if users_collection.find_one({"user_id": user.user_id}):
        raise HTTPException(status_code=400, detail=f"User with user_id {user.user_id} already exists")

    user_dict = user.model_dump()
    result = users_collection.insert_one(user_dict)
    
    response_dict = user.model_dump()
    response_dict["id"] = str(result.inserted_id)
    return User(**response_dict)

@router.get("/users", response_model=list[User])
async def get_users(
    user_id: str = Query(None, description="Filter by user_id"),
    name: str = Query(None),
    phone: str = Query(None),
    is_active: bool = Query(None),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    """
    Retrieves a list of users with optional user_id filter and pagination.
    """
    query = {}
    if user_id:
        query["user_id"] = user_id
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if phone:
        query["phone"] = {"$regex": phone, "$options": "i"}
    if is_active != None:
        query["is_active"] = is_active

    users = []
    cursor = users_collection.find(query).skip(skip).limit(limit)
    
    for doc in cursor:
        doc["id"] = str(doc["_id"])
        users.append(User(**doc))
        
    return users


@router.get("/users/summary", response_model=UserSummary)
async def get_user_summary():
    """
    Returns total number of users and number of active users.
    """
    total = users_collection.count_documents({})
    active = users_collection.count_documents({"is_active": True})

    return UserSummary(
        total_users=total,
        active_users=active
    )


@router.delete("/users")
async def delete_all_detections():
    try:
        docs = users_collection.find({})  # Get all documents

        deleted_count = 0
        for doc in docs:
            image_path = doc.get("image_path")
            if image_path and os.path.exists(image_path):
                try:
                    os.remove(image_path)  # Delete the image file
                except Exception as e:
                    print(f"Error deleting file {image_path}: {e}")
            deleted_count += 1

        users_collection.delete_many({})  # Remove all documents
        return {"message": f"Deleted {deleted_count} users and their images"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))