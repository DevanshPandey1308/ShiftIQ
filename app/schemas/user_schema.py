from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=100)
    email: EmailStr


class UserUpdate(BaseModel):
    username: str = Field(min_length=2, max_length=100)
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }