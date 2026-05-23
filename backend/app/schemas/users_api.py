from pydantic import BaseModel, EmailStr
from datetime import datetime


# What you send when logging in
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# What the server sends back after successful login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Safe user info — never includes password
class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
