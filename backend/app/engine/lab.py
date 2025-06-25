from .greenhouse import Greenhouse
from .logentry import LogEntry
from .timemanager import TimeManager
import copy


class Lab:
    def __init__(self):
        self.greenhouses = {}
        self.time_manager = TimeManager()
        self.log = []
        # Создаем 10 пустых теплиц
        for i in range(10):
            self.add_greenhouse(i)

    def add_greenhouse(self, id: int):
        self.greenhouses[id] = Greenhouse(id)

    def set_plant(self, gh_id: int, plant_type: str):
        if gh_id in self.greenhouses:
            self.greenhouses[gh_id].set_plant(plant_type)

    def remove_plant(self, gh_id: int):
        if gh_id in self.greenhouses:
            self.greenhouses[gh_id].remove_plant()

    def update(self):
        elapsed = self.time_manager.update()
        if elapsed > 0:
            for gh_id, greenhouse in self.greenhouses.items():
                plant = greenhouse.update_plant(elapsed)
                self.log.append(LogEntry(
                    self.time_manager.virtual_time,
                    gh_id,
                    copy.deepcopy(greenhouse.conditions),
                    {
                        'name': plant.name,
                        'stage': plant.stage.value,
                        'size': plant.size,
                        'health': plant.health
                    } if plant is not None else None
                ))

    def step(self):
        elapsed = self.time_manager.step()
        if elapsed > 0:
            for gh_id, greenhouse in self.greenhouses.items():
                plant = greenhouse.update_plant(elapsed)
                self.log.append(LogEntry(
                    self.time_manager.virtual_time,
                    gh_id,
                    copy.deepcopy(greenhouse.conditions),
                    {
                        'name': plant.name,
                        'stage': plant.stage.value,
                        'size': plant.size,
                        'health': plant.health
                    }
                ))

    def get_state(self):
        return {
            'virtual_time': self.time_manager.virtual_time,
            'greenhouses': [
                {
                    'id': gh.id,
                    'conditions': gh.conditions,
                    'plant': {
                        'name': gh.plant.name,
                        'stage': gh.plant.stage.value,
                        'size': gh.plant.size,
                        'health': gh.plant.health,
                        'flowering_percent': gh.plant.flowering_percent
                    } if gh.plant else None  # Обработка пустой теплицы
                } for gh in self.greenhouses.values()
            ]
        }