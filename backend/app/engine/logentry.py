from datetime import datetime
from enum import Enum
import uuid

class LogEventType(Enum):
    PLANT_ADDED = "Посадка растения"
    PLANT_REMOVED = "Удаление растения"
    STAGE_CHANGED = "Смена стадии"
    PLANT_DIED = "Смерть растения"
    CONDITIONS_CHANGED = "Изменение условий"


class LogEntry:
    def __init__(self, timestamp: float, greenhouse_id: int, event_type: LogEventType,
                 conditions: dict = None, plant_data: dict = None, event_details: str = None):
        self.id = str(uuid.uuid4())  # Уникальный идентификатор
        self.timestamp = timestamp
        self.greenhouse_id = greenhouse_id
        self.event_type = event_type
        self.conditions = conditions
        self.plant_data = plant_data
        self.event_details = event_details
        self.real_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'id': self.id,  # Добавляем ID в словарь
            'timestamp': self.timestamp,
            'greenhouse_id': self.greenhouse_id,
            'event_type': self.event_type.value,
            'conditions': self.conditions,
            'plant_data': self.plant_data,
            'event_details': self.event_details,
            'real_time': self.real_time
        }