import matplotlib.pyplot as plt
import numpy as np

# Данные
i = np.array([1, 0, -1, 1, 1])
q = np.array([-1, -1, 0, 0, 1])
omega = 5 * 10 ** 3
fi = np.arctan2(q, i)

# Время
time_interval = 1e-3  # время между отсечками
count = len(i)
t = np.linspace(0, time_interval, 1000)  # общий временной интервал

# Создание фигуры с 3 подграфиками
fig, axs = plt.subplots(3, 1, figsize=(10, 8))

# График 1 (сигнал в форме суммы косинуса и синуса)
for g in range(count):
    T = i[g] * np.cos(2 * np.pi * omega * t) - q[g] * np.sin(2 * np.pi * omega * t)
    axs[0].plot(t + g * time_interval, T, color="green")
axs[0].set_title('Сигнал в форме суммы косинуса и синуса')
axs[0].grid(True)

# График 2 (сигнал с амплитудой и фазой)
for g in range(count):
    a = np.sqrt(q[g] ** 2 + i[g] ** 2)
    T = a * np.cos(2 * np.pi * omega * t + fi[g])
    axs[1].plot(t + g * time_interval, T, color="red")
axs[1].set_title('Сигнал с амплитудой и фазой')
axs[1].grid(True)

# График 3 (сигнал в комплексной форме)
for g in range(count):
    xl = i[g] + 1j * q[g]
    T = np.real(xl * np.exp(2 * np.pi * 1j * omega * t))
    axs[2].plot(t + g * time_interval, T, color="blue")
axs[2].set_title('Комплексный сигнал')
axs[2].grid(True)

# Подгонка подграфиков
plt.tight_layout()
plt.show()
