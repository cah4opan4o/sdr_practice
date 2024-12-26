import numpy as np
import matplotlib.pyplot as plt

# Параметры прямоугольного сигнала
T = 1        # Период сигнала
tau = 0.4    # Длительность импульса
A = 1        # Амплитуда
f_s = 1000   # Частота дискретизации
t = np.arange(0, T, 1 / f_s)  # Временной интервал на период

# Формирование прямоугольного сигнала
x_t = A * ((t % T) < tau).astype(float)

# Число гармоник для анализа
n_harmonics = 6
a_n = []
b_n = []

for n in range(n_harmonics + 1):
    # Опорные гармоники
    cos_n = np.cos(2 * np.pi * n * t / T)
    sin_n = np.sin(2 * np.pi * n * t / T)
    
    # Численное интегрирование для коэффициентов
    an = (2 / T) * np.sum(x_t * cos_n) / f_s
    bn = (2 / T) * np.sum(x_t * sin_n) / f_s
    
    a_n.append(an)
    b_n.append(bn)

# Вычисление амплитуд и фаз
A_n = np.sqrt(np.array(a_n)**2 + np.array(b_n)**2)  # Амплитуды
phi_n = np.arctan2(b_n, a_n)  # Фазы

# Построение спектров
plt.figure(figsize=(10, 6))

# Спектр амплитуд
plt.subplot(2, 1, 1)
plt.stem(range(n_harmonics + 1), A_n, basefmt=" ")
plt.title("Спектр амплитуд (A_n)")
plt.xlabel("Номер гармоники n")
plt.ylabel("Амплитуда")
plt.grid()

# Спектр фаз
plt.subplot(2, 1, 2)
plt.stem(range(n_harmonics + 1), phi_n, basefmt=" ")
plt.title("Спектр фаз (φ_n)")
plt.xlabel("Номер гармоники n")
plt.ylabel("Фаза (рад)")
plt.grid()

plt.tight_layout()
plt.show()

# Синтез временного колебания
t_synth = np.linspace(0, T, f_s)
x_2 = sum(A_n[n] * np.cos(2 * np.pi * n * t_synth / T + phi_n[n]) for n in range(3))  # 2 гармоники
x_4 = sum(A_n[n] * np.cos(2 * np.pi * n * t_synth / T + phi_n[n]) for n in range(5))  # 4 гармоники
x_6 = sum(A_n[n] * np.cos(2 * np.pi * n * t_synth / T + phi_n[n]) for n in range(7))  # 6 гармоник

# Построение временных колебаний
plt.figure(figsize=(10, 6))

plt.plot(t_synth, x_t, label="Оригинальный сигнал", linestyle="dashed")
plt.plot(t_synth, x_2, label="Синтез (2 гармоники)")
plt.plot(t_synth, x_4, label="Синтез (4 гармоники)")
plt.plot(t_synth, x_6, label="Синтез (6 гармоник)")

plt.title("Синтез временного колебания")
plt.xlabel("Время (с)")
plt.ylabel("Амплитуда")
plt.legend()
plt.grid()
plt.show()
