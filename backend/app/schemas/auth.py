from pydantic import BaseModel, EmailStr, Field


class AuthRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: str | None = None
    location: str | None = None


class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class AuthToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
