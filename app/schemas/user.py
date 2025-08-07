from pydantic import BaseModel

class UserBase(BaseModel):
    user_id: str
    name: str
    phone: str
    is_active: bool = True

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str

class UserSummary(BaseModel):
    total_users: int
    active_users: int
