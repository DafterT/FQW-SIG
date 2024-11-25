from controller import Controller
# import matplotlib.pyplot as plt


def main():
    controller = Controller(502.38, 100.456, 627.975, 5)
    controller.static_mode(25, 0.8, 5, 10, 12)
    controller.display_P()
    controller.display_hz()


if __name__ == "__main__":
    main()
