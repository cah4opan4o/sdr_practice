import numpy as np
import matplotlib.pyplot as plt

# Параметры
T = 1  # Период
f1 = 1 / T  # Частота сигнала s1(t)
t = np.linspace(0, T, 1000)  # Временной интервал

# Формирование сигналов
s1 = np.sin(2 * np.pi * f1 * t)
k_values = np.arange(1, 11)  # Значения k для проверки

# Проверка ортогональности
orthogonality_results = []
for k in k_values:
    sk = np.sin(2 * np.pi * k * f1 * t)  # Формируем sk(t)
    integral = np.trapz(s1 * sk, t)  # Вычисляем интеграл через метод трапеций
    orthogonality_results.append((k, integral))

# Вывод результатов
print("Проверка ортогональности для sin(2πf1t) и sin(2πkf1t):")
for k, integral in orthogonality_results:
    print(f"k = {k}, ∫s1(t) * sk(t) dt = {integral:.5f}")

# Построение графиков
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t, s1, label="s1(t) = sin(2πf1t)")
plt.title("Сигнал s1(t)")
plt.xlabel("Время (t)")
plt.ylabel("Амплитуда")
plt.grid()
plt.legend()

plt.subplot(2, 1, 2)
for k in range(1, 4):  # Графики для первых трёх гармоник
    sk = np.sin(2 * np.pi * k * f1 * t)
    plt.plot(t, sk, label=f"sk(t) = sin(2π{k}f1t)")
plt.title("Сигналы sk(t)")
plt.xlabel("Время (t)")
plt.ylabel("Амплитуда")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
