import numpy as np
import matplotlib.pyplot as plt

f_m = 300
f_c = 10 * f_m
f_s = 2 * f_c
t_s = 1 / f_s

t = np.linspace(0, 0.015, 1000)
S_t = 2 * np.cos(2*np.pi*f_m*t) * np.cos(2*np.pi*f_c*t) - np.sin(2*np.pi*f_m*t) * np.sin(2*np.pi*f_c*t)

I = 2*np.cos(2*np.pi*f_m*t)
Q = np.sin(2*np.pi*f_m*t)
z = np.sqrt(I**2 + Q**2)
arg = np.arctan(Q/I)

plt.figure(1)
plt.plot(t,S_t,label='Modulated Signal')
plt.plot(t,z,label='Amplitude of the Signal')
plt.plot(t,arg,label='Phase of the Signal')
plt.grid()
plt.tight_layout()
plt.legend()
 
plt.show()

