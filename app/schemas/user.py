from pydantic import BaseModel

class UserBase(BaseModel):
    user_id: str
    name: str
    phone: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str