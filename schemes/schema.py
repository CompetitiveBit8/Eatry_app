from pydantic import BaseModel, EmailStr

class UserDetails(BaseModel):
    email: EmailStr
    password: str
    role: str

class userLoginDetail(BaseModel):
    email: EmailStr
    password: str