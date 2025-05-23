class PID:
    
    def __init__(self, Kp, Ki, Kd, d_t):
        self.d_t = d_t
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.error = 0.0
        self.integral = 0.0
        self.derivative = 0.0
        self.output = 0.0
        self.previous_error = 0.0
    
    def step(self, target, current):
        self.error = target - current
        self.integral = self.integral + self.error * self.d_t
        self.derivative = (self.error - self.previous_error) / self.d_t
        self.output = self.Kp * self.error + self.Ki * self.integral + self.Kd * self.derivative
        self.previous_error = self.error
        out = max(min(self.output, 100), 25)
        if self.output < 25:
            out = 0
        return out

    def clear(self):
        self.error = 0.0
        self.integral = 0.0
        self.derivative = 0.0
        self.previous_error = 0.0
        self.output = 0.0