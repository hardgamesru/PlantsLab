from .scooter import Scooter
from .person import Person
from .station import Station
from .trip import Trip
import random
import math

class SimulatorEngine:
    """
    Люди сначала ходят к самокату, затем едут до станции,
    после чего останавливаются. Есть состояния: 'walking', 'riding', 'finished'.
    """

    def __init__(self):
        self.people = []
        self.scooters = []
        self.stations = []
        self.trips = []
        self.running = False

    def init_simulation(self, num_people=5, scooters_per_station=3):
        # Очистка
        self.people.clear()
        self.scooters.clear()
        self.trips.clear()

        # Станции
        self.stations = [
            Station(20, 20, capacity=scooters_per_station * 2),
            Station(80, 80, capacity=scooters_per_station * 2),
            Station(20, 80, capacity=scooters_per_station * 2),
            Station(80, 20, capacity=scooters_per_station * 2),
        ]

        # Самокаты у станций
        for st in self.stations:
            for _ in range(scooters_per_station):
                s = Scooter(
                    x=st.x + random.uniform(-2, 2),
                    y=st.y + random.uniform(-2, 2)
                )
                st.scooters.append(s)
                self.scooters.append(s)

        # Люди: спавнятся в любых точках, цель-первая станция,
        # но самокат будет ближний
        for _ in range(num_people):
            x0, y0 = random.uniform(0, 100), random.uniform(0, 100)
            p = Person(x0, y0, None, None)
            # Изначально без цели:
            p.status = 'searching'      # 'searching' → 'walking' → 'riding' → 'finished'
            p.assigned_scooter = None
            p.goal_x = None
            p.goal_y = None
            self.people.append(p)

        self.running = True

    def get_state(self):
        return {
            "people": [vars(p) for p in self.people],
            "scooters": [vars(s) for s in self.scooters],
            "stations": [
                {
                    "x": st.x, "y": st.y,
                    "free_slots": st.capacity - len(st.scooters),
                    "total": st.capacity
                }
                for st in self.stations
            ],
            "trips": [vars(t) for t in self.trips],
            "running": self.running
        }

    def tick(self):
        if not self.running:
            return

        for p in self.people:
            # 1) Человек ищет самокат
            if p.status == 'searching':
                available = [
                    s for s in self.scooters
                    if not s.is_broken
                    and not any(pp.assigned_scooter == s for pp in self.people)
                ]
                if not available:
                    continue
                nearest = min(
                    available,
                    key=lambda s: (s.x - p.x) ** 2 + (s.y - p.y) ** 2
                )
                p.assigned_scooter = nearest
                p.goal_x, p.goal_y = nearest.x, nearest.y
                p.status = 'walking'

            # 2) Человек идёт к самокату
            elif p.status == 'walking':
                self._move_towards(p, p.goal_x, p.goal_y, step=1)
                if self._is_at(p, p.goal_x, p.goal_y, threshold=0.5):
                    # Достиг самоката — теперь выбираем **другую** случайную станцию
                    p.status = 'riding'
                    # Из всех станций убираем ту, вокруг которой он сел
                    other_stations = [
                        st for st in self.stations
                        if math.hypot(st.x - p.x, st.y - p.y) > 0.1
                    ]
                    dest = random.choice(other_stations)
                    p.goal_x, p.goal_y = dest.x, dest.y
                    # Регистрируем поездку
                    trip = Trip(p.id, p.assigned_scooter.id, p.x, p.y, dest.x, dest.y)
                    p.trip = trip
                    self.trips.append(trip)

            # 3) Человек едет на самокате
            elif p.status == 'riding':
                scooter = p.assigned_scooter
                # Передвигаем сначала человека, потом самокат
                self._move_towards(p, p.goal_x, p.goal_y, step=3)
                scooter.move_to(p.x, p.y)
                # Если доехали до станции
                if self._is_at(p, p.goal_x, p.goal_y, threshold=0.5):
                    self._park_scooter(scooter)
                    p.status = 'finished'
                    p.assigned_scooter = None

            # 4) finished — ничего не делаем

    def _move_towards(self, obj, tx, ty, step):
        dx, dy = tx - obj.x, ty - obj.y
        dist = math.hypot(dx, dy)
        if dist <= step or dist == 0:
            obj.x, obj.y = tx, ty
        else:
            ratio = step / dist
            obj.x += dx * ratio
            obj.y += dy * ratio

    def _is_at(self, obj, tx, ty, threshold):
        return math.hypot(obj.x - tx, obj.y - ty) <= threshold

    def _park_scooter(self, scooter):
        nearest_station = min(
            self.stations,
            key=lambda s: (s.x - scooter.x) ** 2 + (s.y - scooter.y) ** 2
        )
        nearest_station.dock(scooter)
