from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import timedelta, datetime
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
SECRET_KEY = "SECRET"

async def password_hash(password):
    return pwd_context.hash()

async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(request: Request, data: dict, expires_delta: timedelta = None):
    print("access token taken over")
    existing_token = request.cookies.get("access_token")
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=0.1))
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def create_refresh_token (request: Request, data: dict, expires_delta: timedelta = None):
    existing_token = request.cookies.get("refresh_token")
    print("refresh token taken over")
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(days=3))
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

# Oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "login")


async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name = payload.get("sub")
        return payload
    except JWTError:
        return None
    
