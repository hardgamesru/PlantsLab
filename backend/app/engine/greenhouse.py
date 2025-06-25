from .plant import Gerbera, Larch


class Greenhouse:
    def __init__(self, id: int, plant_type: str):
        self.id = id
        self.conditions = {
            'temperature': 20.0,
            'humidity': 50.0,
            'light': 70.0,
            'soil': 'loam'
        }
        self.plant = Gerbera() if plant_type == "gerbera" else Larch()

    def update_conditions(self, new_conditions: dict):
        self.conditions.update(new_conditions)

    def update_plant(self, time_elapsed: float):
        self.plant.update(self.conditions, time_elapsed)
        return self.plant