from pydantic import BaseModel, EmailStr

class UserDetails(BaseModel):
    email: EmailStr
    password: str
    # role: str

class userDetail_update(BaseModel):
    email: EmailStr
    password: str