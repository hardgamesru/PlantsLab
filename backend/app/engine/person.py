import uuid

class Person:
    """
    Класс описывает человека (пользователя).
    У него есть стартовые координаты, цель, флаг наличия самоката и объект поездки.
    """

    def __init__(self, start_x: float, start_y: float, goal_x: float, goal_y: float):
        self.id = str(uuid.uuid4())          # Уникальный ID пользователя
        self.x = start_x                     # Текущая позиция (x)
        self.y = start_y                     # Текущая позиция (y)
        self.goal_x = goal_x                 # Цель по X
        self.goal_y = goal_y                 # Цель по Y
        self.has_scooter = False             # Имеет ли самокат сейчас
        self.assigned_scooter = None         # Привязанный самокат (если есть)
        self.trip = None                     # Объект поездки (если активна)
