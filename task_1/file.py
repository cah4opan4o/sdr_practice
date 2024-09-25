import matplotlib.pyplot as plt
import numpy as np
import adi
sdr = adi.Pluto('ip:192.168.2.1') # адрес PlutoSDR
sdr.sample_rate = int(2.6e6) # колчество временных отсчето в 1 [сек]
sdr.buffer_size = int (1024)
# массив на отправку и наприём сигнала
# передать шум - 400 отчётов 2^12 - шум
# считать в матплотлиб
array = []
for i in range(1024):
    if i < 300 or i > 700:
        array.append(complex(0))
    else:
        array.append(complex(4000))

big_array = []
for i in range(1000):
    sdr.tx(array)
    big_array.append(sdr.rx())

plt.subplot(3,1,1)
plt.plot(array)
plt.grid()

plt.subplot(3,1,2)
plt.plot(big_array[1])
plt.grid()

plt.subplot(3,1,3)
plt.plot(big_array)
plt.grid()

plt.show()