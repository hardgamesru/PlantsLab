class Trip:
    """
    Класс описывает поездку.
    Связывает пользователя, самокат и координаты начала/конца поездки.
    """

    def __init__(self, person_id, scooter_id, start_x, start_y, end_x, end_y):
        self.person_id = person_id              # ID пользователя
        self.scooter_id = scooter_id            # ID самоката
        self.start = (start_x, start_y)         # Начальные координаты
        self.end = (end_x, end_y)               # Конечные координаты
        self.distance = 0                       # Пройденное расстояние
        self.finished = False                   # Завершена ли поездка
