from fastapi import APIRouter
from ..engine.engine import SimulatorEngine

router = APIRouter()

# Создаём экземпляр симулятора (глобально)
sim = SimulatorEngine()

@router.post("/start",tags=["Старт программы"])
def start_simulation(people: int = 5, scooters: int = 10):
    """
    Запускает симуляцию: создаёт объекты и подготавливает систему.
    """
    sim.init_simulation(people, scooters)
    return {"status": "started", "people": people, "scooters": scooters}

@router.get("/state")
def get_state():
    """
    Возвращает полное состояние симуляции в текущий момент.
    Используется фронтендом для Canvas.
    """
    return sim.get_state()
@router.get("/tick")
def tick_simulation():
    """
    Продвигает симуляцию на один шаг: перемещает людей, обрабатывает поездки.
    """
    sim.tick()
    return sim.get_state()
