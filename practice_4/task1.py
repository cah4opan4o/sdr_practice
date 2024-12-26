import numpy as np
import matplotlib.pyplot as plt

# Параметры сигнала
A = 2           # Амплитуда
f0 = 5          # Основная частота
T = 1 / f0      # Период
Ts = 0.001      # Шаг по времени
phi = 0         # Начальная фаза
t = np.arange(0, T, Ts)  # Временной интервал на один период

# Гармоническое колебание x(t)
x_t = A * np.cos(2 * np.pi * f0 * t + phi)

# Вычисление коэффициентов ряда Фурье
n_values = range(5)  # Значения n: 0, 1, 2, 3, 4
a_n = []  # Коэффициенты косинусной части
b_n = []  # Коэффициенты синусной части

for n in n_values:
    # Опорные гармоники
    cos_n = np.cos(2 * np.pi * n * f0 * t)
    sin_n = np.sin(2 * np.pi * n * f0 * t)
    
    # Численное интегрирование через сумму
    an = (2 / T) * np.sum(x_t * cos_n) * Ts
    bn = (2 / T) * np.sum(x_t * sin_n) * Ts
    
    a_n.append(an)
    b_n.append(bn)

# Вычисление амплитуд и фаз
A_n = np.sqrt(np.array(a_n)**2 + np.array(b_n)**2)  # Амплитуды
phi_n = np.arctan2(b_n, a_n)  # Фазы

# Построение графиков
plt.figure(figsize=(10, 6))

# Оригинальный сигнал
plt.subplot(3, 1, 1)
plt.plot(t, x_t, label="x(t)")
plt.title("Гармоническое колебание x(t)")
plt.xlabel("Время (s)")
plt.ylabel("Амплитуда")
plt.grid()
plt.legend()

# График амплитуд
plt.subplot(3, 1, 2)
plt.stem(n_values, A_n, basefmt=" ")
plt.title("Амплитуды A_n")
plt.xlabel("Номер гармоники n")
plt.ylabel("Амплитуда")
plt.grid()

# График фаз
plt.subplot(3, 1, 3)
plt.stem(n_values, phi_n, basefmt=" ")
plt.title("Фазы φ_n")
plt.xlabel("Номер гармоники n")
plt.ylabel("Фаза (рад)")
plt.grid()

plt.tight_layout()
plt.show()

# Вывод коэффициентов
for n in n_values:
    print(f"Гармоника {n}: a_{n} = {a_n[n]:.4f}, b_{n} = {b_n[n]:.4f}, A_{n} = {A_n[n]:.4f}, φ_{n} = {phi_n[n]:.4f}")
