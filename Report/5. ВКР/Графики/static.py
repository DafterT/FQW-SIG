import numpy as np
import matplotlib.pyplot as plt

# Numeric mapping for key points
t1, t2, t3, t4,  = 2, 4, 10, 14
t_vals = [0, t1, t2, t2+2, t2+4, t3, t4, t4+1, t4+5]
P_vals = [0, 1, 1, 2, 2, 3, 3, 3.5, 3.5]

plt.figure(figsize=(8, 4))
plt.plot(t_vals, P_vals, color='black', linewidth=2)

# Symbolic ticks only at key points
plt.xticks(
    [0, t1, t2, t3, t4],
    ['0', r'$t_1$', r'$t_2$', r'$t_3$', r'$t_4$']
)
plt.yticks(
    [0, 1, 2, 2.5, 3.5],
    [r'$P_0$', r'$P_1$',r'$P_2$',r'$P_3$', r'$P_4$']
)

plt.xlabel('Время')
plt.ylabel('Давление')
plt.tight_layout()
plt.grid()
plt.savefig('fig/fig_static.png')
plt.show()
