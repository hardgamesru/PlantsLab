from .greenhouse import Greenhouse
from .logentry import LogEntry
from .timemanager import TimeManager
import copy

MAX_LOG_SIZE = 1000  # Максимальный размер журнала

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
            event_type, details = self.greenhouses[gh_id].set_plant(plant_type)
            self.log_event(LogEntry(
                self.time_manager.virtual_time,
                gh_id,
                event_type,
                copy.deepcopy(self.greenhouses[gh_id].conditions),
                None,
                details
            ))

    def remove_plant(self, gh_id: int):
        if gh_id in self.greenhouses:
            event_type, details = self.greenhouses[gh_id].remove_plant()
            self.log_event(LogEntry(
                self.time_manager.virtual_time,
                gh_id,
                event_type,
                copy.deepcopy(self.greenhouses[gh_id].conditions),
                None,
                details
            ))

    def update(self):
        elapsed = self.time_manager.update()
        if elapsed > 0:
            for gh_id, greenhouse in self.greenhouses.items():
                plant, events = greenhouse.update_plant(elapsed)
                for event_type, details in events:
                    self.log_event(LogEntry(
                        self.time_manager.virtual_time,
                        gh_id,
                        event_type,
                        copy.deepcopy(greenhouse.conditions),
                        {
                            'name': plant.name,
                            'stage': plant.stage.value,
                            'size': plant.size,
                            'health': plant.health,
                            'flowering_percent': plant.flowering_percent
                        } if plant else None,
                        details
                    ))

    def step(self):
        elapsed = self.time_manager.step()
        if elapsed > 0:
            for gh_id, greenhouse in self.greenhouses.items():
                plant, events = greenhouse.update_plant(elapsed)
                for event_type, details in events:
                    self.log_event(LogEntry(
                        self.time_manager.virtual_time,
                        gh_id,
                        event_type,
                        copy.deepcopy(greenhouse.conditions),
                        {
                            'name': plant.name,
                            'stage': plant.stage.value,
                            'size': plant.size,
                            'health': plant.health,
                            'flowering_percent': plant.flowering_percent
                        } if plant else None,
                        details
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

    def get_greenhouse_states(self):
        return [gh for gh in self.greenhouses.values()]

    def log_event(self, event: LogEntry):
        # Ограничиваем размер журнала
        if len(self.log) >= MAX_LOG_SIZE:
            self.log.pop(0)
        self.log.append(event)

    def clear_log(self):
        self.log = []

    def remove_log_entry(self, index: int):
        if 0 <= index < len(self.log):
            self.log.pop(index)