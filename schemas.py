from pydantic import BaseModel, Field

class UserBase(BaseModel):
    name: str  = Field(..., max_length=50)

class User(UserBase):
    id: int

class UserCreate(UserBase):
    firebase_uid: str = Field(..., max_length=128)

class UserUpdate(UserBase):
    name: str | None = None