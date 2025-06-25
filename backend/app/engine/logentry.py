class LogEntry:
    def __init__(self, timestamp: float, greenhouse_id: int, conditions: dict, plant_data: dict):
        self.timestamp = timestamp
        self.greenhouse_id = greenhouse_id
        self.conditions = conditions
        self.plant_data = plant_data