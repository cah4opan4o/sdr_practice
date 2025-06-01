import numpy as np
import matplotlib.pyplot as plt

def symbol_synchronization(signal, guard_interval_len, num_symbols, symbol_len):
    correlation = []
    start_indices = []
    for i in range(len(signal) - guard_interval_len):
        similarity = np.linalg.norm(signal[i:i + guard_interval_len] - guard_interval)
        correlation.append(similarity)
        if np.allclose(signal[i:i + guard_interval_len], guard_interval, atol=1e-6):
            start_indices.append(i)
            if len(start_indices) == num_symbols:
                break
    return start_indices, correlation

T = 1e-4  # Длительность символа
Nc = 64  # Количество поднесущих
symbols_count = 4  # Количество передаваемых OFDM-символов
pilot_interval = 3  # Интервал пилотов
pilot_value = 1 + 1j  # Пилотный символ

# Формирование поднесущих
sc_matr = np.zeros((Nc, Nc), dtype=complex)
for k in range(Nc):
    sc_matr[k, :] = 1 / np.sqrt(T) * np.exp(1j * 2 * np.pi * k * (1 / T) * np.arange(Nc) * (T / Nc))

# Формирование данных с пилотами
data = np.sign(np.random.rand(symbols_count, Nc) - 0.5) + 1j * np.sign(np.random.rand(symbols_count, Nc) - 0.5)
for i in range(Nc):
    if i % pilot_interval == 0:
        data[:, i] = pilot_value

# OFDM-модуляция
ofdm_symbols = np.fft.ifft(data, axis=1)
guard_interval_len = int(0.3 * Nc)
guard_interval = ofdm_symbols[:, -guard_interval_len:]
ofdm_symbols_with_guard = np.hstack((guard_interval, ofdm_symbols))

# Передача через канал с шумом
signal_length = ofdm_symbols_with_guard.shape[1]
noise = (np.random.randn(symbols_count, 2 * signal_length) + 1j * np.random.randn(symbols_count, 2 * signal_length)) * 0.1
noisy_signal = noise.copy()
start_symbol = 43
for i in range(symbols_count):
    noisy_signal[i, start_symbol + i * signal_length:start_symbol + (i + 1) * signal_length] = ofdm_symbols_with_guard[i]

# Символьная синхронизация
sync_indices, correlation = symbol_synchronization(noisy_signal[0], guard_interval_len, symbols_count, signal_length)

# Декодирование символов
rx_symbols = []
for sync_index in sync_indices:
    rx_signal = noisy_signal[:, sync_index + guard_interval_len:sync_index + guard_interval_len + Nc]
    rx_symbols.append(np.fft.fft(rx_signal, axis=1))
rx_symbols = np.array(rx_symbols)

# Интерполяция канала
H_LS = noisy_signal[:, pilot_interval::pilot_interval] / pilot_value  # Оценка на пилотах
H_c = np.zeros_like(rx_symbols, dtype=complex)

for i in range(H_LS.shape[1] - 1):
    a, b = i * pilot_interval, (i + 1) * pilot_interval
    H_a, H_b = H_LS[:, i], H_LS[:, i + 1]
    for c in range(a, b):
        H_c[:, c] = H_a + (H_b - H_a) * (c - a) / (b - a)
H_c[:, :pilot_interval] = H_LS[:, 0]
H_c[:, -pilot_interval:] = H_LS[:, -1]

# Коррекция принятого сигнала
X_e = rx_symbols / H_c

# Визуализация
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(correlation, label='Correlation with Guard Interval')
plt.axvline(sync_indices[0], color='r', linestyle='--', label='Detected Start Index')
plt.legend()
plt.title("Symbol Synchronization - Detection of Start Index")
plt.xlabel("Sample Index")
plt.ylabel("Correlation Value")
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(X_e[0].real, label='Re(Recovered Signal)')
plt.plot(X_e[0].imag, label='Im(Recovered Signal)')
plt.legend()
plt.title("Recovered OFDM Symbols after Interpolation")
plt.xlabel("Subcarrier Index")
plt.ylabel("Amplitude")
plt.grid()

plt.show()
