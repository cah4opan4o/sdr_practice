import matplotlib.pyplot as plt
import numpy as np
import adi  # Библиотека для работы с PlutoSDR

# Инициализация PlutoSDR
sdr = adi.Pluto('ip:192.168.2.1')  # Адрес PlutoSDR
sdr.sample_rate = int(2.6e6)       # Количество временных отсчетов в секунду
sdr.buffer_size = int(1024)        # Размер буфера

# Формирование массива для передачи сигнала
array = []
for i in range(1024):
    if i < 300 or i > 700:
        array.append(complex(0))  # Добавляем нулевой сигнал
    else:
        array.append(complex(4000))  # Добавляем сигнал с амплитудой 4000

# Прием сигнала
big_array = []
for i in range(1000):
    sdr.tx(array)  # Передача массива
    big_array.append(sdr.rx())  # Прием массива

# Построение графиков
plt.subplot(2, 1, 1)
plt.plot(array)  # График переданного сигнала
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(big_array[1])  # График принятого сигнала
plt.grid()

plt.show()
