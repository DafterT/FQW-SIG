from controller import Controller
# import matplotlib.pyplot as plt


def cycle_test():
    controller = Controller((49.98, 4.996, 62.475), (600, 50, 100), 0.1, True)
    controller.cycle_mode(10, 1.5, 5)
    controller.cycle_mode(27, 1.5, 5)
    controller.model.P = 10
    controller.model.P_noise = 10
    controller.P_vals = [controller.model.P_noise] * 10
    controller.cycle_mode(27, 1.5, 5)
    controller.display_P()
    controller.display_hz()
    controller.display_speed()
    
def static_test():
    controller = Controller((49.98, 4.996, 62.475), (600, 50, 100), 0.1, True)
    controller.static_mode(27, 0.3, 5, 10, 12.5)
    controller.model.P = 12
    controller.model.P_noise = 12
    controller.P_vals = [controller.model.P_noise] * 10
    controller.static_mode(27, 1.5, 5, 10, 12.5)
    controller.display_P()
    controller.display_hz()
    controller.display_speed()
    

def test():
    controller = Controller((10, 0.01, .5), (0, 0, 0), 100, True)
    controller.static_mode(5, 2, 1, 10, 12.5, .5, False)
    controller.display_P()
    controller.display_hz()
    controller.display_speed()
    


if __name__ == "__main__":
    # cycle_test()
    test()
