from fastapi import FastAPI, status, Depends, HTTPException, Response
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from utils.auth_utils import get_current_user, password_hash, verify_password, create_access_token, create_refresh_token
from schemes.schema import UserDetails
from database.database import get_db
from models.model_user import UserTable
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


app = FastAPI(title="Food Ordering App")

@app.get("/")
async def root():
    return {"Message": "Welcome home"}

@app.post("/signUp")
async def sign_Up(user: UserDetails, db: AsyncSession = Depends(get_db)):
    stmnt = select(UserTable).where(UserTable.email == user.email)
    result = await db.execute(stmnt)
    user_info = result.scalar()

    if user_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    # hashed_password = password_hash(user.password)
    new_users = UserTable(email=user.email, password=user.password, role=user.role)
    db.add(new_users)
    await db.commit()
    await db.refresh(new_users)
    return {"message": f"New user added with email as {new_users.email} was added"}


@app.post("/login")
async def login(request: Request, user: UserDetails, response: Response, db: AsyncSession = Depends(get_db)):
    stmnt = select(UserTable).where(UserTable.email == user.email)
    result = await db.execute(stmnt)
    user_info = result.scalar()

    if not user_info:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User deteails incorrect")
    if not user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User details incorrect")
    
    token_data = {"sub": user_info.email, "role": user_info.role}
    access_token = create_access_token(request=request, data=token_data)
    refresh_token = create_refresh_token(request=request, data=token_data)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/protected")
async def protected_routes(current_user =  Depends(get_current_user)):
    # role = UserTable.role
    return {"message": "You have entered a protected route", 
            "user": current_user}


@app.patch("/update_user_info")
async def user_update(user: UserDetails, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    stmt = select(UserTable).where(UserTable.email == current_user.email)
    result = await db.execute(stmt)
    user_info = result.scalar_one_or_none()
    
    # print(current_user)
    # print(user_info.email)

    if not user_info:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised attempt")
    
    # if not verify_password(user.password, user_info.password)
    
    user_info.email = user.email
    user_info.password = password_hash(user.password)

    print(user_info)

    # db.add(user_info)
    await db.commit()
    await db.refresh(user_info)
    return {"message": "User information successfully updated"}
    
@app.post("/logout")
async def logout(response: Response, n = Depends(get_db)):
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}