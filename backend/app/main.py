from fastapi import FastAPI
from .routers import scooters
from .database import Base, engine

app = FastAPI(title="Scooter Share API")

Base.metadata.create_all(bind=engine)  # Автосоздание таблиц

app.include_router(scooters.router, prefix="/api", tags=["scooters", "stations"])
