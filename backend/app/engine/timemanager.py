import time


class TimeManager:
    def __init__(self):
        self.time_scale = 1.0
        self.paused = True
        self.last_update_time = time.time()
        self.virtual_time = 0.0

    def update(self):
        if not self.paused:
            # Увеличиваем виртуальное время на масштаб
            self.virtual_time += self.time_scale
            return self.time_scale
        return 0.0

    def set_time_scale(self, scale: float):
        self.time_scale = scale

    def toggle_pause(self):
        self.paused = not self.paused
        if not self.paused:
            self.last_update_time = time.time()

    def step(self):
        if self.paused:
            step_elapsed = 1.0 * self.time_scale
            self.virtual_time += step_elapsed
            return step_elapsed
        return 0.0