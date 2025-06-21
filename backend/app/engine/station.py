class Station:
    """
    Класс описывает станцию парковки самокатов.
    У неё есть координаты, максимальная ёмкость и список текущих самокатов.
    """

    def __init__(self, x: float, y: float, capacity: int):
        self.x = x                          # Координаты станции
        self.y = y
        self.capacity = capacity            # Максимальное число самокатов
        self.scooters = []                  # Список припаркованных самокатов

    def has_space(self):
        """Проверка: есть ли свободное место"""
        return len(self.scooters) < self.capacity

    def dock(self, scooter):
        """
        Парковка самоката: если есть место, добавляем в список.
        """
        if self.has_space():
            self.scooters.append(scooter)
            return True
        return False
