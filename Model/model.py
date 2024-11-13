from math import tan


class Model:
    def __init__(self, dt):
        self.dt = dt  # Размер шага в модели
        self.t = 0  # Текущее время в модели
        self.P = 0  # Текущее давление в модели
        self.hz_hist = [0]
        self.P_hist = [0]
        self.t_hist = [0]

    def update(self, hz, is_drain=True, is_engine=True):
        self.P -= self.drain(is_drain)
        self.P += self.engine(hz, is_engine)
        self.P = min(max(self.P, 0), 100)
        self.t += self.dt
        self.P_hist.append(self.P)
        self.hz_hist.append(hz)
        self.t_hist.append(self.t)

    def drain(self, is_drain):
        return (self.P * 0.0025 + 0.01) * self.dt if is_drain else 0

    def engine(self, hz, is_engine):
        return tan(hz / 57.3) * self.dt * 0.1 if is_engine else 0


"""
TODO:
1. Снять данные для 20, 30, 40 Гц и посмотреть на динамику для drain и engine.
"""
