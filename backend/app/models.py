from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location_x = Column(Float)
    location_y = Column(Float)
    capacity = Column(Integer)

    scooters = relationship("Scooter", back_populates="station")


class Scooter(Base):
    __tablename__ = "scooters"

    id = Column(Integer, primary_key=True, index=True)
    battery_level = Column(Integer)  # от 0 до 100
    is_broken = Column(Boolean, default=False)

    station_id = Column(Integer, ForeignKey("stations.id"))
    station = relationship("Station", back_populates="scooters")
