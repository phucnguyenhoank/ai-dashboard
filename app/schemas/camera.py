from pydantic import BaseModel

class CameraBase(BaseModel):
    camera_id: str
    name: str
    base64: str | None = None  # Included in input/response, not stored in DB
    short_description: str
    details_description: str

class CameraCreate(CameraBase):
    pass

class Camera(CameraBase):
    id: str
    image_path: str | None = None  # Stored in DB

class CameraWithStats(Camera):
    unread_detections: int

class CameraSummary(BaseModel):
    total_cameras: int
    active_cameras: int