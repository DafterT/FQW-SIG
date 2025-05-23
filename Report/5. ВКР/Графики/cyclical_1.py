import numpy as np
import matplotlib.pyplot as plt

# Dummy numeric values for plotting
P1 = 0
P2 = 1
t1 = 1
t2 = 0.5

# Generate the rising segment
x_rise = np.linspace(0, t1, 100)
y_rise = np.linspace(P1, P2, 100)

# Generate the plateau segment
x_plateau = np.linspace(t1, t1 + t2, 100)
y_plateau = np.full_like(x_plateau, P2)

# Plotting
plt.figure()
plt.plot(x_rise, y_rise)
plt.plot(x_plateau, y_plateau)

# Remove numeric ticks and set only symbolic labels
plt.xticks([0, t1, t1 + t2], ['0', r'$t_1$', r'$t_1 + t_2$'])
plt.yticks([P1, P2], [r'$P_1$', r'$P_2$'])

# Optional: label axes
plt.xlabel('Время')
plt.ylabel('Давление')
plt.grid()
plt.savefig('fig/fig_cyclical_1.png')
plt.show()
