import uuid
import random

class Scooter:
    """
    Класс описывает электросамокат.
    У него есть уникальный ID, координаты, заряд батареи и состояние (исправен или сломан).
    """

    def __init__(self, x: float, y: float):
        # Уникальный идентификатор для самоката
        self.id = str(uuid.uuid4())
        # Координаты на карте
        self.x = x
        self.y = y
        # Начальный заряд
        self.battery_level = 100
        # Флаг состояния
        self.is_broken = False

    def move_to(self, x: float, y: float):
        """
        Метод перемещает самокат в указанные координаты, если он исправен.
        При этом расходуется заряд и с некоторой вероятностью самокат ломается.
        """
        if not self.is_broken:
            self.x = x
            self.y = y
            self.battery_level -= random.randint(1, 5)  # Расход батареи
            # Случайная поломка (например, 5%)
            if random.random() < 0.05:
                self.is_broken = True
