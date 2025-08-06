from fastapi import APIRouter, HTTPException, Query
from app.schemas.user import UserCreate, User
from app.core.database import users_collection
from bson import ObjectId

router = APIRouter(prefix="/ai", tags=["users"])

@router.post("/users", response_model=User)
async def create_user(user: UserCreate):
    """
    Creates a new user.
    """
    if users_collection.find_one({"user_id": user.user_id}):
        raise HTTPException(status_code=400, detail=f"User with user_id {user.user_id} already exists")

    user_dict = user.dict()
    result = users_collection.insert_one(user_dict)
    
    response_dict = user.dict()
    response_dict["id"] = str(result.inserted_id)
    return User(**response_dict)

@router.get("/users", response_model=list[User])
async def get_users(
    user_id: str = Query(None, description="Filter by user_id"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    """
    Retrieves a list of users with optional user_id filter and pagination.
    """
    query = {}
    if user_id:
        query["user_id"] = user_id

    users = []
    cursor = users_collection.find(query).skip(skip).limit(limit)
    
    for doc in cursor:
        doc["id"] = str(doc["_id"])
        users.append(User(**doc))
        
    return users