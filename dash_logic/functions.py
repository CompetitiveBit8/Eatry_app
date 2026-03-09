from models.model_user import UserTable, food_table
from fastapi import Depends
from schemes.schema import userLoginDetail
from schemes.food_schemas import foodDetails
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def update_details(user: userLoginDetail):
    stmnt = select(UserTable).where(UserTable.email == user.email)
    result = await db.execute(stmnt)
    user_info = result.scalar()

async def show_dishes(menu: foodDetails, db: AsyncSession = Depends()):
    stmnt = select(food_table).where(food_table.food == menu.food)
    result = await db.execute(stmnt)
    food_info = result.scalar()
    return {"food": food_info.food, "quantity_available": food_info.quantity_available}
     

def show_pending_orders():
        pass

def fund_account():
      pass