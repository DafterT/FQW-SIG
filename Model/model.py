from random import random

class Model:
    def __init__(self, dt, activate_noise=True):
        self.dt = dt  # Размер шага в модели в ms
        self.t = 0  # Текущее время в модели
        self.P = 0  # Текущее давление в модели
        self.P_noise = 0
        self.activate_noise = activate_noise 
        
        self.counter = 0

    def update(self, percent, is_drain=True, is_engine=True):
        for _ in range(self.dt):
            self.P += self.drain(is_drain) / 1000 + self.engine(percent, is_engine) / 1000
            self.P = max(self.P, 0)
        self.P_noise = self.P + ((random() * 0.02 - 0.01) if self.activate_noise else 0)
    
    def drain(self, is_drain):
        return 0.09556781 / (self.P + 4.19694606) - 0.02272167 if is_drain else 0

    def engine(self, percent, is_engine):
        return 0.02865982 * percent / 60 if is_engine else 0

    def clear(self):
        self.t = 0
        self.P = 0
        self.P_noise = 0
