from model import Model
import matplotlib.pyplot as plt


def main():
    model = Model(1)
    for _ in range(1000):
        model.update(50)
    plt.plot(model.t_hist, model.P_hist)
    plt.show()
    plt.plot(model.t_hist, model.hz_hist)
    plt.show()


if __name__ == "__main__":
    main()
