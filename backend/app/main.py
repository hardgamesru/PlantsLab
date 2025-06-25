from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import simulation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulation.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Plant Simulation API"}