import numpy as np
import matplotlib.pyplot as plt

# Функция символьной синхронизации Эвклидово расстояние
def symbol_synchronization(signal, guard_interval_len):
    correlation = []
    for i in range(len(signal) - guard_interval_len):
        similarity = np.linalg.norm(signal[i:i + guard_interval_len] - guard_interval)
        correlation.append(similarity)
        if np.allclose(signal[i:i + guard_interval_len], guard_interval, atol=1e-6):
            return i, correlation  # Возвращаем индекс начала основного сигнала и корреляцию
    return -1, correlation  # Если не найдено

T = 1 * np.e**(-4)  # Длительность символа
Nc = 128  # Количество поднесущих
df = 1 / T  # Частотный интервал между поднесущими
ts = T / Nc  # Интервал дискретизации
x_symbols = []
num_symbols = 5  # Количество символов для передачи

for i in range(num_symbols):
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
    x_symbols = np.concatenate((x_symbols, xt2_with_guard))

# Создание массива в 2 раза больше сигнала, заполненного шумом
signal_length = len(x_symbols)
noise = (np.random.randn(2 * signal_length) + 1j * np.random.randn(2 * signal_length)) * 0.1
noisy_signal = noise.copy()
noisy_signal[23:23 + signal_length] = x_symbols  # Вставка нашего сигнала на 23 индекс

plt.figure(2)
for i in range(num_symbols):
    sync_index, correlation = symbol_synchronization(noisy_signal, guard_interval_len)
    print(f"Символьная синхронизация: индекс начала основного сигнала = {sync_index}")

    # Прием символа на Nc поднесущих при помощи ДПФ принятого символа
    sr2 = np.sqrt(T) / Nc * np.fft.fft(noisy_signal[sync_index:sync_index + len(sd_with_pilots)*num_symbols])

    plt.subplot(5,1,i+1)
    plt.scatter(sr2.real, sr2.imag)
    plt.grid()

# Визуализация корреляции
plt.figure(3, figsize=(10, 5))
plt.subplot(2, 1, 1)
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

plt.show()
