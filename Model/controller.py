from model import Model
from PID import PID
import matplotlib.pyplot as plt

class Controller:
    
    def __init__(self, kP, kI, kD, d_t=1):
        self.model = Model(d_t)
        self.PID = PID(kP, kI, kD, d_t)
        self.d_t = d_t
        self.t = 0
        self.hz_hist = [0]
        self.P_hist = [0]
        self.P_noise_hist = [0]
        self.target_hist = [0]
        self.t_hist = [0]
        
    def do_step(self, current, target):
        percent = self.PID.step(target, current)
        self.model.update(percent)
        self.t += self.d_t
        self.hz_hist.append(percent)
        self.P_hist.append(self.model.P)
        self.P_noise_hist.append(self.model.P_noise)
        self.target_hist.append(target)
        self.t_hist.append(self.t)

    def cycle_mode(self, P_max, v_filling, time):
        t = 0
        start_P = self.model.P_noise
        t_filling = (P_max - start_P) / (v_filling / 60)
        
        while self.model.P <= P_max - 0.1:
            target = t * (P_max - start_P) / t_filling + start_P
            target = min(target, P_max)
            self.do_step(self.model.P_noise, target)
            t += self.d_t
        
        self.PID.clear()
        
        t = 0
        while t < time * 60:
            target = P_max
            self.do_step(self.model.P_noise, target)
            t += self.d_t
            

    def display_P(self):
        plt.plot(self.t_hist, self.P_hist, label='Давление')
        plt.plot(self.t_hist, self.P_noise_hist, label='Давление + шум')
        plt.plot(self.t_hist, self.target_hist, label='Целевое давление')
        plt.legend()
        plt.show()
    
    def display_hz(self):
        plt.plot(self.t_hist, self.hz_hist)
        plt.show()