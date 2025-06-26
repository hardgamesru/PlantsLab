from fastapi import APIRouter, HTTPException


from ..engine.lab import Lab  # Измененный импорт
import json

router = APIRouter()
lab = Lab()


@router.get("/state")
async def get_state():
    lab.update()
    return lab.get_state()


@router.post("/pause")
async def toggle_pause():
    lab.time_manager.toggle_pause()
    return {"status": "paused" if lab.time_manager.paused else "running"}


@router.post("/step")
async def step():
    lab.step()
    return {"status": "step executed"}


@router.post("/time_scale/{scale}")
async def set_time_scale(scale: float):
    if scale < 0.1 or scale > 1000.0:
        raise HTTPException(status_code=400, detail="Invalid scale value")
    lab.time_manager.set_time_scale(scale)
    return {"status": "scale updated"}


@router.post("/greenhouse/{gh_id}/conditions")
async def update_conditions(gh_id: int, conditions: dict):
    if gh_id not in lab.greenhouses:
        raise HTTPException(status_code=404, detail="Greenhouse not found")

    allowed_keys = {'temperature', 'humidity', 'light', 'soil'}
    if not set(conditions.keys()).issubset(allowed_keys):
        raise HTTPException(status_code=400, detail="Invalid conditions")

    lab.greenhouses[gh_id].update_conditions(conditions)
    return {"status": "conditions updated"}


@router.post("/greenhouse/{gh_id}/plant/{plant_type}")
async def set_plant(gh_id: int, plant_type: str):
    if gh_id not in lab.greenhouses:
        raise HTTPException(status_code=404, detail="Greenhouse not found")
    if plant_type not in ["gerbera", "larch"]:
        raise HTTPException(status_code=400, detail="Invalid plant type")

    lab.set_plant(gh_id, plant_type)
    return {"status": "plant added"}


@router.delete("/greenhouse/{gh_id}/plant")
async def remove_plant(gh_id: int):
    if gh_id not in lab.greenhouses:
        raise HTTPException(status_code=404, detail="Greenhouse not found")

    lab.remove_plant(gh_id)
    return {"status": "plant removed"}


@router.post("/reset")
async def reset_system():
    global lab
    lab = Lab()  # При перезапуске создаем новую лабораторию с пустыми теплицами
    # Возвращаем кнопку паузы в исходное состояние
    lab.time_manager.paused = True
    return {
        "status": "system reset",
        "paused": True
    }
