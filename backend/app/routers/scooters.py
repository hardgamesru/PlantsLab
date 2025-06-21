from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# STATIONS
@router.get("/stations", response_model=List[schemas.Station])
def list_stations(db: Session = Depends(get_db)):
    return crud.get_stations(db)

@router.post("/stations", response_model=schemas.Station)
def add_station(station: schemas.StationCreate, db: Session = Depends(get_db)):
    return crud.create_station(db, station)

# SCOOTERS
@router.get("/", response_model=List[schemas.Scooter])
def list_scooters(db: Session = Depends(get_db)):
    return crud.get_scooters(db)

@router.post("/", response_model=schemas.Scooter)
def add_scooter(scooter: schemas.ScooterCreate, db: Session = Depends(get_db)):
    return crud.create_scooter(db, scooter)
