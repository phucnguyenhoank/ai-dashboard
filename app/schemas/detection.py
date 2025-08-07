from pydantic import BaseModel
from datetime import datetime

class DetectionBase(BaseModel):
    type: str
    base64: str  | None = None # Included in the input and response, but not stored in DB
    lat: float
    long: float
    timestamp: datetime
    seen: bool = False
    camera_id: str
    user_id: str

# input
class DetectionCreate(DetectionBase):
    camera_name: str
    user_name: str

# output
class Detection(DetectionCreate):
    id: str
    image_path: str | None = None
