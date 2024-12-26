import numpy as np
import matplotlib.pyplot as plt

# Входная последовательность бит
bits = np.array([1, 1, 0, 1, 1, 1, 1, 0, 1, 0])

# Параметры
N = 10  # Коэффициент оверсэмплинга
h = np.ones(N)  # Фильтр с АЧХ {1, 1, ..., 1} длиной N

# Преобразование битов для QPSK
bits = 2 * bits - 1  # Преобразование в значения {-1, 1}

# Разделение на I и Q компоненты
xi = bits[0::2]  # Реальная часть (I)
xq = bits[1::2]  # Мнимая часть (Q)

# Оверсэмплинг с нулевым заполнением
xi_oversampled = np.zeros(len(xi) * N)  # Создаём массив для оверсэмплированных данных
xq_oversampled = np.zeros(len(xq) * N)

xi_oversampled[::N] = xi  # Записываем значения xi через каждые N
xq_oversampled[::N] = xq  # Записываем значения xq через каждые N

# Применение фильтрации (свёртка с h)
xi_filtered = np.convolve(xi_oversampled, h, mode='full')
xq_filtered = np.convolve(xq_oversampled, h, mode='full')

# Масштабирование для достижения амплитуды 2^11
scaling_factor = 2**11
xi_filtered *= scaling_factor
xq_filtered *= scaling_factor

# преобразование в int16
real_part = (xi_filtered).astype(np.int16)
imag_part = (xq_filtered).astype(np.int16)

# Комплексный сигнал после фильтрации
x_bb = real_part + 1j * imag_part



# Запись результата в файл
with open("scam.txt", "w") as file:
    for i in range(len(x_bb)):
        file.write(f"{x_bb[i].real}  {x_bb[i].imag}\n")

print("Результаты сохранены в файл 'scam.txt'.")

# Визуализация
plt.figure(figsize=(14, 8))

# Исходный сигнал
plt.subplot(3, 2, 1)
plt.stem(bits)
plt.title("Input Bits")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.grid()

# I и Q компоненты после оверсэмплинга
plt.subplot(3, 2, 3)
plt.plot(xi_oversampled, label='Oversampled I')
plt.plot(xq_oversampled, label='Oversampled Q', linestyle='--')
plt.title("Oversampled Signal (I and Q)")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()

# Сигнал I и Q после фильтрации
plt.subplot(3, 2, 5)
plt.plot(xi_filtered, label='Filtered I')
plt.plot(xq_filtered, label='Filtered Q', linestyle='--')
plt.title("Filtered Signal (I and Q)")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()

# Созвездие QPSK после фильтрации
plt.subplot(1, 2, 2)
plt.scatter(x_bb.real, x_bb.imag, c='r')
plt.title("QPSK Constellation (Filtered)")
plt.xlabel("In-phase (I)")
plt.ylabel("Quadrature (Q)")
plt.grid()

plt.tight_layout()
plt.show()

