from pydantic import BaseModel
from typing import Optional

class StationBase(BaseModel):
    name: str
    location_x: float
    location_y: float
    capacity: int

class StationCreate(StationBase):
    pass

class Station(StationBase):
    id: int

    class Config:
        orm_mode = True


class ScooterBase(BaseModel):
    battery_level: int
    is_broken: bool = False
    station_id: Optional[int]

class ScooterCreate(ScooterBase):
    pass

class Scooter(ScooterBase):
    id: int

    class Config:
        orm_mode = True
