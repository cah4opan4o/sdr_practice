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

def gardner_ted(I,Q,Nsp,Ns):
    ted = 0.0
    for n in range(0, len(I) - Nsp - Ns):
        ted += (I[n+Nsp+Ns]-I[n+Ns])*I[n+Nsp//2+Ns]+(Q[n+Nsp+Ns]-Q[n+Ns])*Q[n+Nsp//2+Ns]
        print(ted)
    return ted

def resample_signal(I, Q, offset):
    new_I, new_Q = [], []
    for i in range(len(I) - int(offset) - 1):
        index = int(i + offset)
        if index < len(I):
            new_I.append(I[index])
            new_Q.append(Q[index])
    return np.array(new_I), np.array(new_Q)

def update_offset(offset, step_offset, timming_error):
    new_offset = offset - step_offset * timming_error
    return new_offset


if __name__ == "__main__":
    file_path = "/home/plutosdr/Desktop/ia232/sdr/samples/data/txdata.pcm"
    Nsp = 10 # sample per symbol
    Ns = 0 # shift
    offset = 0
    step_offset = 0.01


    I,Q = read_file(file_path)

    # Приведение к -1 и 1, max=2**11
    I = I / max(abs(I))
    Q = Q / max(abs(Q))

    filter = np.ones(10)
    I = np.convolve(I,filter,mode='same')
    Q = np.convolve(Q,filter,mode='same')

    # num_taps = 101  # Длина фильтра
    # roll_off = 0.35  # Коэффициент скругления (0.2–0.5)
    # symbol_rate = 1/Nsp  # Скорость символов
    # nyquist_rate = 0.5  # Нормализованная частота Найквиста

    # rrc_filter = firwin(num_taps, symbol_rate * (1 + roll_off), fs=1.0)

    # # Применение фильтрации к I и Q
    # I_filt = lfilter(rrc_filter, 1.0, I)
    # Q_filt = lfilter(rrc_filter, 1.0, Q)
    
    # QPSK before Gardner 
    plt.figure(figsize=(16,8))
    plt.subplot(1,2,1)
    plt.scatter(Q,I)
    plt.title("QPSK before Gardner")

    
    timing_error = gardner_ted(I, Q, Nsp, Ns)
    offset = update_offset(offset, timing_error, step_offset)
    I, Q = resample_signal(I, Q, offset)
    
    # QPSK after Gardner
    plt.subplot(1,2,2)
    plt.scatter(Q,I)
    plt.title("QPSK after Gardner")

    plt.show()