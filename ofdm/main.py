import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft , ifft , fftshift
import scipy.interpolate

# Функция символьной синхронизации
def symbol_synchronization(signal, guard_interval_len):
    correlation = []
    for i in range(len(signal) - guard_interval_len):
        similarity = np.linalg.norm(signal[i:i + guard_interval_len] - guard_interval)
        correlation.append(similarity)
        if np.allclose(signal[i:i + guard_interval_len], guard_interval, atol=1e-6):
            return i, correlation  # Возвращаем индекс начала основного сигнала и корреляцию
    return -1, correlation  # Если не найдено

T = 1 * np.e**(-4)  # Длительность символа
Nc = 64  # Количество поднесущих
df = 1 / T  # Частотный интервал между поднесущими
ts = T / Nc  # Интервал дискретизации
symbols_count = 4
start_symbol = 43

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

pilots_index = []
sd_with_pilots = []
for i in range(len(sd)):
    sd_with_pilots.append(sd[i])
    if (i + 1) % pilot_interval == 0:
        sd_with_pilots.append(pilot_value)  # Вставка пилота
        pilots_index.append(i+1)

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
noisy_signal[start_symbol:start_symbol + signal_length] = xt2_with_guard  # Вставка нашего сигнала на 7 индекс

sync_index, correlation = symbol_synchronization(noisy_signal, guard_interval_len)
print(f"Символьная синхронизация: индекс начала основного сигнала = {sync_index}")
rx_signal = noisy_signal[sync_index+guard_interval_len:]
symbol = rx_signal[:len(sd_with_pilots)]

# Выполняем FFT и масштабирование
sr2 = np.sqrt(T) / Nc * np.fft.fft(symbol)

# # Выделяем индексы пилотных сигналов и соответствующие значения
# pilot_indices = np.array(pilots_index)  # Индексы пилотных символов
# pilot_values = sr2[pilot_indices]  # Значения пилотов после FFT

# # Определяем индексы всех поднесущих
# all_indices = np.arange(len(sr2))

# # Выполняем линейную интерполяцию по пилотным тонам
# interp_real = scipy.interpolate.interp1d(pilot_indices, pilot_values.real, kind='linear', fill_value="extrapolate")
# interp_imag = scipy.interpolate.interp1d(pilot_indices, pilot_values.imag, kind='linear', fill_value="extrapolate")

# # Восстанавливаем значения несущих
# sr2_interp = interp_real(all_indices) + 1j * interp_imag(all_indices)

# Оценка канала на пилотных поднесущих
H_LS = noisy_signal[pilots_index] / pilot_value  # H_LS[k] = Y(pilot_loc(k)) / Xp(k)

# Линейная интерполяция без библиотек
H_c = np.zeros(len(sr2), dtype=complex)

for i in range(len(pilots_index) - 1):
    a, b = pilots_index[i], pilots_index[i + 1]
    H_a, H_b = H_LS[i], H_LS[i + 1]
    
    for c in range(a, b):
        H_c[c] = H_a + (H_b - H_a) * (c - a) / (b - a)

# Заполнение концов массива, если нужно
H_c[:pilots_index[0]] = H_LS[0]
H_c[pilots_index[-1]:] = H_LS[-1]

# Коррекция принятого сигнала
X_e = sr2 / H_c



# Визуализация корреляции
plt.figure(1,figsize=(10, 5))
plt.subplot(4,1,1)
plt.plot(correlation, label='Correlation with Guard Interval')
plt.axvline(sync_index, color='r', linestyle='--', label='Detected Start Index')
plt.legend()
plt.title("Symbol Synchronization - Detection of Start Index")
plt.xlabel("Sample Index")
plt.ylabel("Correlation Value")
plt.grid()

# Визуализация OFDM-сигнала с шумом
plt.subplot(4,1,2)
plt.plot(noisy_signal.real, label='Re(Noisy Signal)')
plt.plot(noisy_signal.imag, label='Im(Noisy Signal)')
plt.axvline(sync_index, color='r', linestyle='--', label='Detected Start Index')
plt.legend()
plt.title("Noisy Signal with OFDM Symbol")
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.grid()

plt.subplot(4,1,3)
plt.plot(sr2.real,label='Re(Noisy Signal)')
plt.plot(sr2.imag,label='Im(Noisy Signal)')
plt.title("Before interpolate") 
plt.legend()

plt.subplot(4,1,4)
plt.plot(X_e.real,label='Re(Noisy Signal)')
plt.plot(X_e.imag,label='Im(Noisy Signal)')
plt.title("after interpolate") 
plt.legend()

plt.show()