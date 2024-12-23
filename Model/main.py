from controller import Controller
from controller import WINDOW_SPEED
# import matplotlib.pyplot as plt


def cycle_test():
    controller = Controller((10, 0.01, .5), (60, .5, 1), 100, True)
    controller.cycle_mode(10, 1.5, 5, False)
    controller.cycle_mode(27, 1.5, 5, False)
    controller.model.P = 10
    controller.model.P_noise = 10
    controller.P_vals = [controller.model.P_noise] * WINDOW_SPEED
    controller.cycle_mode(27, 1.5, 5, False)
    controller.display_P()
    controller.display_hz()
    controller.display_speed()
    
def static_test():
    controller = Controller((10, 0.01, .5), (0, 0, 0), 100, True)
    controller.static_mode(27, 1, 5, 10, 12.5, 0.5, is_drain=False)
    controller.model.P = 12
    controller.model.P_noise = 12
    controller.P_vals = [controller.model.P_noise] * WINDOW_SPEED
    controller.static_mode(27, 2, 5, 10, 12.5, 0.5, is_drain=False)
    controller.display_P()
    controller.display_hz()
    controller.display_speed()
    

def test():
    controller = Controller((10, 0.01, .5), (60, .5, 1), 100, True)
    controller.static_mode(10, 2, 5, 10, 12.5, .5, False)
    controller.display_P()
    controller.display_hz()
    controller.display_speed()
    


if __name__ == "__main__":
    cycle_test()
