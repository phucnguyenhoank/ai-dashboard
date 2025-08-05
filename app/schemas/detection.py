from pydantic import BaseModel
from datetime import datetime

class DetectionBase(BaseModel):
    type: str
    base64: str
    lat: float
    long: float
    timestamp: datetime
    seen: bool
    camera_id: str
    user_id: str

class DetectionCreate(DetectionBase):
    pass

class Detection(DetectionBase):
    id: str