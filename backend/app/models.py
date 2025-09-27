from sqlalchemy import Column, Integer, Text, Date, TIMESTAMP
from sqlalchemy.sql import func
from backend.app.db import Base

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    user_name = Column(Text)
    user_phone = Column(Text)
    date = Column(Date)
    time_slot = Column(Text)
    status = Column(Text, default="CONFIRMED")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
