from database.database import Base

class foodDetails(Base):
    food: str
    date: str
    quantity_available: int

