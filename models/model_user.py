from database.database import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime

class UserTable(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)
    role = Column(String, index=True)
   

class RefreshTokenTable(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))  # link to your user table
    token = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)