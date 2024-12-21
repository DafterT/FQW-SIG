from model import Model
from PID import PID
import matplotlib.pyplot as plt

WINDOW_SPEED = 50

class Controller:

    def __init__(self, speed_coef, P_coef, d_t=1, activate_noise=True):
        self.model = Model(d_t, activate_noise)
        self.PID_speed = PID(*speed_coef, d_t)
        self.PID_P = PID(*P_coef, d_t)
        self.d_t = d_t
        self.t = 0
        self.hz_hist = [0]
        self.P_hist = [0]
        self.P_noise_hist = [0]
        self.target_hist = [0]
        self.t_hist = [0]
        self.P_vals = [self.model.P_noise] * WINDOW_SPEED
        self.average_speed = 0

    def do_step(self, PID, current, target, is_drain=True):
        percent = PID.step(target, current)
        self.model.update(percent, is_drain)
        self.t += self.d_t
        self.hz_hist.append(percent)
        self.P_hist.append(self.model.P)
        self.P_noise_hist.append(self.model.P_noise)
        self.target_hist.append(self.average_speed * 60)
        self.t_hist.append(self.t / 1000)
        
        self.P_vals = [self.model.P_noise] + self.P_vals[:-1]
        speed_mas = []
        self.average_speed = 0
        for i, j in zip(self.P_vals[:(WINDOW_SPEED // 2)], self.P_vals[(WINDOW_SPEED) // 2:]):
            speed_mas.append((i - j) / (WINDOW_SPEED // 2) * 1000 / self.d_t)
        self.average_speed = sum(speed_mas) / len(speed_mas)

    def cycle_mode(self, P_max, v_filling, time, is_drain=True):
        while self.model.P_noise <= P_max:
            counter += 1
            self.do_step(self.PID_speed, self.average_speed * 60, v_filling, is_drain)
        self.PID_speed.clear()
        
        t = 0
        while t < time * 60 * 1000:
            self.do_step(self.PID_P, self.model.P_noise, P_max, is_drain)
            t += self.d_t
        self.PID_P.clear()
    
    def static_mode(self, P_max, v_filling, t_1, t_2, P_interim, d_P = 5, is_drain=True):
        t = 0
        start_P = self.model.P_noise
        end_P = self.model.P_noise

        while end_P != P_max:
            start_P = end_P
            end_P = start_P + d_P
            if end_P > P_max:
                end_P = P_max

            while self.model.P_noise <= end_P:
                self.do_step(self.PID_speed, self.average_speed * 60, v_filling, is_drain)
            
            self.PID_speed.clear()
            
            t = 0
            t_control = t_1 * 60 * 1000
            if end_P >= P_interim:
                t_control = t_2 * 60 * 1000
            while t <= t_control:
                self.do_step(self.PID_P, self.model.P_noise, end_P, is_drain)
                t += self.d_t
            self.PID_P.clear()

        
    def display_P(self):
        plt.plot(self.t_hist, self.P_hist, label='Давление')
        plt.plot(self.t_hist, self.P_noise_hist, label='Давление + шум')
        plt.legend()
        plt.grid()
        plt.show()
    
    def display_hz(self):
        plt.plot(self.t_hist, self.hz_hist)
        plt.show()
        
    def display_speed(self):
        plt.plot(self.t_hist, self.target_hist, label='Целевое давление')
        plt.show()
        
    def clear_controller(self):
        self.PID.clear()
        self.model.clear()
        self.t = 0
        self.hz_hist = [0]
        self.P_hist = [0]
        self.P_noise_hist = [0]
        self.target_hist = [0]
        self.t_hist = [0]