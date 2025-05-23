import numpy as np
import matplotlib.pyplot as plt

# Dummy numeric values for plotting
P1 = 0
P2 = 1
P3 = 0.2
t1 = 1
t2 = 0.5
t3 = 0.1

# Generate the rising segment
x_rise = np.linspace(0, t1, 100)
y_rise = np.linspace(P1, P2, 100)

# Generate the plateau segment
x_plateau = np.linspace(t1, t1 + t2, 100)
y_plateau = np.full_like(x_plateau, P2)

# сброс
x_valve = np.linspace(t1 + t2, t1 + t2 + t3, 100)
y_valve = np.linspace(P2, P3, 100)
x = t1 + t2 + t3
plt.figure()
plt.plot(x_rise, y_rise, color='black')
plt.plot(x_plateau, y_plateau, color='black')
plt.plot(x_valve, y_valve, color='black')

# Generate the rising segment
x_rise = np.linspace(x, x + t1 - 0.2, 100)
y_rise = np.linspace(P3, P2, 100)

# Generate the plateau segment
x_plateau = np.linspace(x + t1 - 0.2, x + t1 - 0.2 + t2, 100)
y_plateau = np.full_like(x_plateau, P2)

# сброс
x_valve = np.linspace(x + t1 - 0.2 + t2, x + t1 - 0.2 + t2 + t3, 100)
y_valve = np.linspace(P2, P3, 100)
x = x + t1 - 0.2 + t2 + t3
plt.plot(x_rise, y_rise, color='black')
plt.plot(x_plateau, y_plateau, color='black')
plt.plot(x_valve, y_valve, color='black')

# Generate the rising segment
x_rise = np.linspace(x, x + t1 - 0.2, 100)
y_rise = np.linspace(P3, P2, 100)

# Generate the plateau segment
x_plateau = np.linspace(x + t1 - 0.2, x + t1 - 0.2 + t2, 100)
y_plateau = np.full_like(x_plateau, P2)

# сброс
x_valve = np.linspace(x + t1 - 0.2 + t2, x + t1 - 0.2 + t2 + t3, 100)
y_valve = np.linspace(P2, P3, 100)

plt.plot(x_rise, y_rise, color='black')
plt.plot(x_plateau, y_plateau, color='black')
plt.plot(x_valve, y_valve, color='black')
# Remove numeric ticks and set only symbolic labels
plt.xticks([0], ["0"])
plt.yticks([P1, P2], [r"$P_1$", r"$P_2$"])

# Optional: label axes
plt.xlabel("Время")
plt.ylabel("Давление")
plt.grid()
plt.savefig("fig/fig_cyclical_2.png")
plt.show()
