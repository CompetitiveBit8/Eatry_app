from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./user.db"

async_engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread":False}, pool_size=5,max_overflow=5, echo=True)

sessionLocal = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = sessionLocal()
    try:
        yield db
    finally:
        await db.close()
        