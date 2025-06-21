from fastapi import FastAPI
from .routers import simulator

app = FastAPI(title="Scooter Simulation API")

# Подключаем маршруты
app.include_router(simulator.router, prefix="/api")
