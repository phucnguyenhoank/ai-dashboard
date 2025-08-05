from pydantic import BaseModel
from datetime import datetime
from typing import List

class DetectionDetail(BaseModel):
    person_id: str
    hard_hat: bool
    location: str

class DetectionCreate(BaseModel):
    timestamp: datetime
    location: str
    total_people: int
    hard_hats_detected: int
    violations: int
    detection_details: List[DetectionDetail]

class Detection(DetectionCreate):
    id: str  # MongoDB uses _id as a string (ObjectId)