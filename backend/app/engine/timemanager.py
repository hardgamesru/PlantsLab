import time


class TimeManager:
    def __init__(self):
        self.time_scale = 1.0
        self.paused = True
        self.last_update_time = time.time()
        self.virtual_time = 0.0

    def update(self):
        if not self.paused:
            current_time = time.time()
            real_elapsed = current_time - self.last_update_time
            virtual_elapsed = real_elapsed * self.time_scale
            self.virtual_time += virtual_elapsed
            self.last_update_time = current_time
            return virtual_elapsed
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