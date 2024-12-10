from controller import Controller
# import matplotlib.pyplot as plt


def cycle_test():
    controller = Controller((49.98, 4.996, 62.475), (600, 50, 100), 1, True)
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
    controller = Controller((49.98, 4.996, 62.475), (600, 50, 100), 1, False)
    controller.static_mode(27, 0.3, 5, 10, 12.5)
    controller.model.P = 10
    controller.model.P_noise = 10
    controller.P_vals = [controller.model.P_noise] * 10
    controller.static_mode(27, 1.5, 5, 10, 12.5)
    controller.display_P()
    controller.display_hz()
    controller.display_speed()
    


if __name__ == "__main__":
    static_test()
