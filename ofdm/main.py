import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft , ifft , fftshift

# bit_to_symbol = {
#     "0000": (-3, -3), "0001": (-3, -1), "0011": (-3, +1), "0010": (-3, +3),
#     "0100": (-1, -3), "0101": (-1, -1), "0111": (-1, +1), "0110": (-1, +3),
#     "1100": (+1, -3), "1101": (+1, -1), "1111": (+1, +1), "1110": (+1, +3),
#     "1000": (+3, -3), "1001": (+3, -1), "1011": (+3, +1), "1010": (+3, +3)
# }

# bit_array = np.random.randint(0, 2, (16,4))

# bit_strings = ["".join(map(str,bits)) for bits in bit_array]

# symbols = np.array([bit_to_symbol[bits] for bits in bit_strings])

# I, Q = symbols[:, 0], symbols[:, 1]

# plt.figure(1,figsize=(6, 6))
# plt.scatter(I, Q, color="blue", marker="o")

# # Подписываем точки
# for i, bits in enumerate(bit_strings):
#     plt.text(I[i], Q[i], bits, fontsize=10, ha='right', va='bottom')

# plt.axhline(0, color="black", linewidth=1)
# plt.axvline(0, color="black", linewidth=1)
# plt.xlim(-4, 4)
# plt.ylim(-4, 4)
# plt.grid(True, linestyle="--", linewidth=0.5)
# plt.title("Созвездие QAM-16")

# -------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

T = 1 * np.e**(-4)  # Длительность символа
Nc = 16  # Количество поднесущих
df = 1 / T  # Частотный интервал между поднесущими
ts = T / Nc  # Интервал дискретизации

t = ts * np.arange(0, Nc)
sc_matr = np.zeros((Nc, len(t)), dtype=complex)

# Матрица из поднесущих
for k in range(Nc):
    sc_matr[k, :] = 1 / np.sqrt(T) * np.exp(1j * 2 * np.pi * k * df * t)

# Формирование передаваемых данных (Nc комплексных символов)
sd = np.sign(np.random.rand(Nc) - 0.5) + 1j * np.sign(np.random.rand(Nc) - 0.5)

# Вставка пилотных сигналов (единицы) каждые 3 символа
pilot_value = 1 + 1j
pilot_interval = 3

sd_with_pilots = []
for i in range(len(sd)):
    sd_with_pilots.append(sd[i])
    if (i + 1) % pilot_interval == 0:
        sd_with_pilots.append(pilot_value)  # Вставка пилота

sd_with_pilots = np.array(sd_with_pilots)

# Формирование OFDM-сигнала с пилотами
xt = np.zeros((1, len(t)), dtype=complex)
for k in range(len(sd_with_pilots)):
    sc = sc_matr[k % Nc, :]
    xt = xt + sd_with_pilots[k] * sc

xt = xt.reshape(Nc)

# Применение IFFT
xt2 = np.fft.ifft(sd_with_pilots, len(sd_with_pilots))

# Добавление защитного интервала (30% хвоста сигнала)
guard_interval_len = int(0.3 * len(xt2))
guard_interval = xt2[-guard_interval_len:]  # Хвостовая часть
xt2_with_guard = np.concatenate((guard_interval, xt2))

# Создание массива в 2 раза больше сигнала, заполненного шумом
signal_length = len(xt2_with_guard)
noise = (np.random.randn(2 * signal_length) + 1j * np.random.randn(2 * signal_length)) * 0.1
noisy_signal = noise.copy()
noisy_signal[7:7 + signal_length] = xt2_with_guard  # Вставка нашего сигнала на 7 индекс

# Функция символьной синхронизации
def symbol_synchronization(signal, guard_interval_len):
    correlation = []
    for i in range(len(signal) - guard_interval_len):
        similarity = np.linalg.norm(signal[i:i + guard_interval_len] - guard_interval)
        correlation.append(similarity)
        if np.allclose(signal[i:i + guard_interval_len], guard_interval, atol=1e-6):
            return i, correlation  # Возвращаем индекс начала основного сигнала и корреляцию
    return -1, correlation  # Если не найдено

sync_index, correlation = symbol_synchronization(noisy_signal, guard_interval_len)
print(f"Символьная синхронизация: индекс начала основного сигнала = {sync_index}")

# Визуализация корреляции
plt.figure(1,figsize=(10, 5))
plt.subplot(2,1,1)
plt.plot(correlation, label='Correlation with Guard Interval')
plt.axvline(sync_index, color='r', linestyle='--', label='Detected Start Index')
plt.legend()
plt.title("Symbol Synchronization - Detection of Start Index")
plt.xlabel("Sample Index")
plt.ylabel("Correlation Value")
plt.grid()

# Визуализация OFDM-сигнала с шумом
plt.subplot(2,1,2)
plt.plot(noisy_signal.real, label='Re(Noisy Signal)')
plt.plot(noisy_signal.imag, label='Im(Noisy Signal)')
plt.axvline(sync_index, color='r', linestyle='--', label='Detected Start Index')
plt.legend()
plt.title("Noisy Signal with OFDM Symbol")
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.grid()
plt.show()