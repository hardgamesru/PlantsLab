from .logentry import LogEventType
from .plant import Gerbera, Larch, Cactus, Orchid, Sunflower, Flytrap, SaguaroCactus, Rafflesia


class Greenhouse:
    # Словарь классов растений
    PLANT_CLASSES = {
        "gerbera": Gerbera,
        "larch": Larch,
        "cactus": Cactus,
        "orchid": Orchid,
        "sunflower": Sunflower,
        "flytrap": Flytrap,
        "saguaro": SaguaroCactus,
        "rafflesia": Rafflesia
    }

    def __init__(self, id: int):
        self.id = id
        self.conditions = {
            'temperature': 20.0,
            'humidity': 50.0,
            'light': 70.0,
            'soil': 'loam'
        }
        self.plant = None  # Начальное состояние - без растения

    DEFAULT_CONDITIONS = {
        'temperature': 20.0,
        'humidity': 50.0,
        'light': 70.0,
        'soil': 'loam'
    }

    def set_plant(self, plant_type: str):
        # Получаем класс растения из словаря
        plant_class = self.PLANT_CLASSES.get(plant_type)
        if not plant_class:
            return None  # Неизвестный тип растения

        # Создаем экземпляр растения
        self.plant = plant_class()

        # Используем имя растения из созданного экземпляра
        plant_name = self.plant.name

        # Записываем событие посадки
        return LogEventType.PLANT_ADDED, f"Посажено растение: {plant_name}"

    def remove_plant(self):
        plant_name = self.plant.name if self.plant else "Неизвестное растение"
        self.plant = None
        self.conditions = self.DEFAULT_CONDITIONS.copy()

        # Записываем событие удаления
        return LogEventType.PLANT_REMOVED, f"Удалено растение: {plant_name}"

    def update_plant(self, time_elapsed: float):
        if self.plant:
            old_stage = self.plant.stage
            self.plant.update(self.conditions, time_elapsed)
            new_stage = self.plant.stage

            # Возвращаем растение и список событий
            return self.plant, self.plant.check_for_events(new_stage, old_stage)
        return None, []

    def update_conditions(self, new_conditions: dict):
        self.conditions.update(new_conditions)

