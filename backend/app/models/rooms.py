# app/models/rooms.py
from sqlalchemy import Column, Integer, DateTime
from db.base import Base

class RoomsByDate(Base):
    __tablename__ = "rooms_by_date"

    fecha = Column("fecha", DateTime, primary_key=True)
    rooms_reserved = Column("rooms_reserved", Integer, nullable=False)
