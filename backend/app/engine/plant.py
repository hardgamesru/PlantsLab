from enum import Enum
from abc import ABC, abstractmethod

from .logentry import LogEventType


class LifeStage(Enum):
    SEED = "Семя"
    SPROUT = "Росток"
    GROWING = "Рост"
    MATURE = "Взрослое растение"
    FLOWERING = "Цветение"
    DEAD = "Мертвое"  # Добавлена новая стадия


class Plant(ABC):
    def __init__(self, name: str, growth_rate: float = 1.0):
        self.name = name
        self.growth_rate = growth_rate  # Коэффициент роста
        self.stage = LifeStage.SEED
        self.size = 0.1
        self.health = 100.0
        self.time_without_flowering = 0.0
        self.flowering_percent = 0.0  # Процент цветения
        # Оптимальные показатели (задаются в подклассах)
        self.optimal_temperature = 20.0
        self.optimal_humidity = 50.0
        self.optimal_light = 50.0
        self.health_change_rate = 1.0  # Скорость изменения здоровья

    def check_health(self, conditions: dict, time_elapsed: float):
        # Проверка отклонений от оптимальных условий с порогом ±30
        temp_diff = max(0, abs(conditions['temperature'] - self.optimal_temperature) - 10)
        humidity_diff = max(0, abs(conditions['humidity'] - self.optimal_humidity) - 20)
        light_diff = max(0, abs(conditions['light'] - self.optimal_light) - 30)

        # Суммарное отклонение (только за пределами порога)
        total_diff = temp_diff + humidity_diff + light_diff

        # Изменение здоровья в зависимости от условий
        if total_diff == 0:
        # Хорошие условия: здоровье растет
            self.health = min(100.0, (self.health + self.health_change_rate * time_elapsed))
        else:
        # Ухудшение здоровья пропорционально отклонению
            self.health -= (total_diff / 100) * self.health_change_rate * time_elapsed

        # Если здоровье <= 0, растение умирает
        if self.health <= 0:
            self.stage = LifeStage.DEAD
            self.health = 0.0

    def calculate_growth_modifier(self, conditions: dict):
        """Рассчитывает модификатор роста на основе отклонения условий"""
        temp_diff = abs(conditions['temperature'] - self.optimal_temperature)
        humidity_diff = abs(conditions['humidity'] - self.optimal_humidity)
        light_diff = abs(conditions['light'] - self.optimal_light)

        # Суммарное отклонение (нормализованное)
        total_diff = temp_diff + humidity_diff + light_diff
        # Модификатор роста: 1.0 при идеальных условиях, уменьшается с отклонением
        return max(0.1, 1.0 - total_diff / 100)

    def check_for_events(self, new_stage: LifeStage, old_stage: LifeStage):
        events = []

        # Событие смены стадии
        if new_stage != old_stage:
            events.append((
                LogEventType.STAGE_CHANGED,
                f"Стадия изменена: {old_stage.value} → {new_stage.value}"
            ))

        # Событие смерти растения
        if new_stage == LifeStage.DEAD and old_stage != LifeStage.DEAD:
            events.append((
                LogEventType.PLANT_DIED,
                "Растение погибло"
            ))

        return events

    @abstractmethod
    def update(self, conditions: dict, time_elapsed: float):
        pass


class Gerbera(Plant):
    def __init__(self):
        super().__init__("Гербера", growth_rate=1.0)
        self.optimal_temperature = 22.0
        self.optimal_humidity = 60.0
        self.optimal_light = 70.0
        self.flowering_temp = 22.0
        self.health_change_rate = 2.0  # Быстрее реагирует на изменения

    def update(self, conditions: dict, time_elapsed: float):
        # Проверяем здоровье перед обновлением
        self.check_health(conditions, time_elapsed)
        effective_time = time_elapsed * self.growth_rate
        growth_modifier = self.calculate_growth_modifier(conditions)

        # Если растение мертвое, прекращаем обновление
        if self.stage == LifeStage.DEAD:
            return

        if self.stage == LifeStage.SEED and conditions['humidity'] > 60:
            self.stage = LifeStage.SPROUT
        elif self.stage == LifeStage.SPROUT and conditions['light'] > 50:
            self.stage = LifeStage.GROWING
            self.size = 0.5
        elif self.stage == LifeStage.GROWING and self.size < 5.0:
            self.size += 0.1 * conditions['light'] / 100 * effective_time * growth_modifier
            self.time_without_flowering += time_elapsed
            if (self.time_without_flowering >= 20) and (conditions['temperature'] >= self.flowering_temp):
                self.time_without_flowering = 0
                self.stage = LifeStage.FLOWERING

        elif self.stage == LifeStage.GROWING and self.size >= 5.0:
            self.stage = LifeStage.MATURE
        elif self.stage == LifeStage.FLOWERING:
            # Увеличиваем процент цветения
            self.flowering_percent = min(100.0, self.flowering_percent + 10 * time_elapsed)
            if self.flowering_percent == 100:
                self.flowering_percent = 0.0
                if self.size < 5.0:
                    self.stage = LifeStage.GROWING
                else:
                    self.stage = LifeStage.MATURE

        elif self.stage == LifeStage.MATURE:
            self.time_without_flowering += time_elapsed
            if (self.time_without_flowering >= 20) and (conditions['temperature'] >= self.flowering_temp):
                self.time_without_flowering = 0
                self.stage = LifeStage.FLOWERING




class Larch(Plant):
    def __init__(self):
        super().__init__("Лиственница", growth_rate=0.3)
        self.optimal_temperature = 18.0
        self.optimal_humidity = 50.0
        self.optimal_light = 60.0
        self.stratification_required = True
        self.stratified = False
        self.stratification_time = 0.0
        self.health_change_rate = 0.5  # Медленнее реагирует на изменения

    def update(self, conditions: dict, time_elapsed: float):
        # Проверяем здоровье перед обновлением
        self.check_health(conditions, time_elapsed)
        effective_time = time_elapsed * self.growth_rate
        growth_modifier = self.calculate_growth_modifier(conditions)

        # Если растение мертвое, прекращаем обновление
        if self.stage == LifeStage.DEAD:
            return

        if not self.stratified and conditions['temperature'] < 5:
            self.stratification_time += time_elapsed
            if self.stratification_time >= 5.0:
                self.stratified = True

        if self.stage == LifeStage.SEED and self.stratified:
            self.stage = LifeStage.SPROUT
        elif self.stage == LifeStage.SPROUT and conditions['humidity'] > 40:
            self.stage = LifeStage.GROWING
        elif self.stage == LifeStage.GROWING:
            self.size += 0.05 * effective_time * growth_modifier
            self.time_without_flowering += time_elapsed
            if (self.time_without_flowering >= 50):
                self.time_without_flowering = 0
                self.stage = LifeStage.FLOWERING
            if self.size > 8.0:
                self.stage = LifeStage.MATURE

        elif self.stage == LifeStage.FLOWERING:
            # Увеличиваем процент цветения
            self.flowering_percent = min(100.0, self.flowering_percent + 10 * time_elapsed)
            if self.flowering_percent == 100:
                self.flowering_percent = 0.0
                if self.size < 8.0:
                    self.stage = LifeStage.GROWING
                else:
                    self.stage = LifeStage.MATURE

        elif self.stage == LifeStage.MATURE:
            self.time_without_flowering += time_elapsed
            if (self.time_without_flowering >= 50):
                self.time_without_flowering = 0.0
                self.stage = LifeStage.FLOWERING

