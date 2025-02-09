import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, lfilter

def read_file(file_path):
    dtype = np.int16
    with open(file_path, "rb") as file:
        data = np.fromfile(file, dtype=dtype)
    I = data[0::2]
    Q = data[1::2]
    return I,Q

# def gardner_ted(I,Q,Nsp,Ns):
#     ted = 0.0
#     for n in range(0, len(I) - Nsp - Ns):
#         ted += (I[n+Nsp+Ns]-I[n+Ns])*I[n+Nsp//2+Ns]+(Q[n+Nsp+Ns]-Q[n+Ns])*Q[n+Nsp//2+Ns]

#     return ted

# def resample_signal(I, Q, offset):
#     new_I, new_Q = [], []
#     for i in range(len(I) - int(offset) - 1):
#         index = int(i + offset)
#         if index < len(I):
#             new_I.append(I[index])
#             new_Q.append(Q[index])
#     return np.array(new_I), np.array(new_Q)

# def update_offset(offset, step_offset, timming_error):
#     new_offset = offset - step_offset * timming_error
#     return new_offset


def gardner_timing_recovery(I, Q, Nsps, BnTs=0.01, zeta=1.0, Kp=1.0):
    # Вычисление параметров K1, K2
    theta = (BnTs * Nsps) / (zeta + 1 / (4 * zeta))
    K1 = (-4 * theta**2) / ((1 + 2 * zeta * theta + theta**2) * Kp)
    K2 = (-4 * theta**2) / ((1 + 2 * zeta * theta + theta**2) * Kp)
    
    # Начальная инициализация переменных
    p1 = 0
    p2 = 0
    offset = 0  # Начальное смещение
    recovered_I = []
    recovered_Q = []
    
    for n in range(len(I) - 2 * Nsps):
        e = (I[n + Nsps - Nsps] - I[n + Nsps]) * \
            (Q[n + Nsps // 2 + Nsps] - Q[n + Nsps // 2 - Nsps])
        
        # Обновление p1, p2
        p1 = e * K1
        p2 += p1 + e * K2
        
        # Коррекция задержки
        if p2 >= 1:
            p2 -= 1
        elif p2 <= -1:
            p2 += 1
        
        # Определение текущего индекса выборки
        offset = round(p2 * Nsps)
        sample_index = n + offset
        
        # Проверка границ
        if 0 <= sample_index < len(I):
            recovered_I.append(I[sample_index])
            recovered_Q.append(Q[sample_index])
    
    return np.array(recovered_I), np.array(recovered_Q)



if __name__ == "__main__":
    file_path = "D:\\Github\\sdr_practice\\gardner\\data\\txdata.pcm"
    Nsp = 10 # sample per symbol
    Ns = 0 # shift
    offset = 0
    step_offset = 0.01


    I,Q = read_file(file_path)


    # Приведение к -1 и 1, max=2**11
    I = I / max(abs(I))
    Q = Q / max(abs(Q))

    plt.figure(figsize=(16,8))
    plt.subplot(3,2,1)
    plt.title("raw data")
    plt.plot(Q,label="Q")
    plt.plot(I,label="I")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.legend()
    
    filter = np.ones(10)
    I = np.convolve(I,filter,mode='valid')
    Q = np.convolve(Q,filter,mode='valid')
    
    plt.subplot(3,2,2)
    plt.title("after filter")
    plt.plot(Q,label="Q")
    plt.plot(I,label="I")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.legend()
    
    # QPSK before Gardner 
    plt.subplot(3,2,3)
    plt.scatter(Q,I)
    plt.title("QPSK before Gardner")

    # /////////////////////////////////////////////////////////////////////////
    output_I, output_Q = gardner_timing_recovery(I, Q, Nsp) # Nsp = Nsps
    # /////////////////////////////////////////////////////////////////////////
    
    # QPSK after Gardner
    plt.subplot(3,2,4)
    plt.scatter(output_Q, output_I)
    plt.title("QPSK after Gardner")
    
    plt.grid()
    plt.show()