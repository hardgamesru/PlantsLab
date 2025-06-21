from sqlalchemy.orm import Session
from . import models, schemas

# STATIONS
def get_stations(db: Session):
    return db.query(models.Station).all()

def create_station(db: Session, station: schemas.StationCreate):
    db_station = models.Station(**station.dict())
    db.add(db_station)
    db.commit()
    db.refresh(db_station)
    return db_station

# SCOOTERS
def get_scooters(db: Session):
    return db.query(models.Scooter).all()

def create_scooter(db: Session, scooter: schemas.ScooterCreate):
    db_scooter = models.Scooter(**scooter.dict())
    db.add(db_scooter)
    db.commit()
    db.refresh(db_scooter)
    return db_scooter
