from .plant import Gerbera, Larch

class Greenhouse:
    def __init__(self, id: int):
        self.id = id
        self.conditions = {
            'temperature': 20.0,
            'humidity': 50.0,
            'light': 70.0,
            'soil': 'loam'
        }
        self.plant = None  # Начальное состояние - без растения

    def set_plant(self, plant_type: str):
        if plant_type == "gerbera":
            self.plant = Gerbera()
        elif plant_type == "larch":
            self.plant = Larch()

    def remove_plant(self):
        self.plant = None

    def update_conditions(self, new_conditions: dict):
        self.conditions.update(new_conditions)

    def update_plant(self, time_elapsed: float):
        if self.plant:
            self.plant.update(self.conditions, time_elapsed)
            return self.plant
        return None