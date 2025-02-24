import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft , ifft , fftshift

bit_to_symbol = {
    "0000": (-3, -3), "0001": (-3, -1), "0011": (-3, +1), "0010": (-3, +3),
    "0100": (-1, -3), "0101": (-1, -1), "0111": (-1, +1), "0110": (-1, +3),
    "1100": (+1, -3), "1101": (+1, -1), "1111": (+1, +1), "1110": (+1, +3),
    "1000": (+3, -3), "1001": (+3, -1), "1011": (+3, +1), "1010": (+3, +3)
}

bit_array = np.random.randint(0, 2, (16,4))

bit_strings = ["".join(map(str,bits)) for bits in bit_array]

symbols = np.array([bit_to_symbol[bits] for bits in bit_strings])

I, Q = symbols[:, 0], symbols[:, 1]

plt.figure(1,figsize=(6, 6))
plt.scatter(I, Q, color="blue", marker="o")

# Подписываем точки
for i, bits in enumerate(bit_strings):
    plt.text(I[i], Q[i], bits, fontsize=10, ha='right', va='bottom')

plt.axhline(0, color="black", linewidth=1)
plt.axvline(0, color="black", linewidth=1)
plt.xlim(-4, 4)
plt.ylim(-4, 4)
plt.grid(True, linestyle="--", linewidth=0.5)
plt.title("Созвездие QAM-16")



T=1*np.e**(-4) # Длительность символа
Nc=16 # Количество поднесущих
df=1/T # Частотный интервал между поднесущими
ts=T/Nc # Интервал дискретизации


k=1
t=ts*np.arange(0 ,Nc)
s=1/np.sqrt (T)*np.exp(1j*2*np.pi*k*df*t) # Формирование одной поднесущей с частотой f*df
plt.figure(2)
plt.plot(t, s.real) #реальная часть поднесущей
plt.plot(t,s.imag)
sc_matr = np.zeros ((Nc,len(t)) , dtype=complex)
sd = np.zeros ((1 ,Nc) , dtype=complex)
# Матрица из поднесуших
for k in range(Nc):
    sk_k=1/np.sqrt (T)*np.exp(1j*2*np.pi*k*df*t)
    sc_matr[k,:]=sk_k
#sd − вектор Nc передаваемых комплексных символов
sd=np.sign(np.random.rand(1 ,Nc) -0.5)+1j*np.sign(np.random.rand(1 ,Nc) -0.5)
sd=sd.reshape(Nc)
xt=np.zeros((1 ,len(t)) , dtype=complex)
# формирование суммы модулированных поднесущих
for k in range (Nc):
    sc=sc_matr[k , : ]
    xt=xt+sd[k] * sc
    xt=xt.reshape(Nc)
# реальная часть сформированного OFDM символа
plt.figure (3)
plt.plot (t, xt.real)
plt.plot (t, xt.imag)

xt2=np.fft.ifft(sd ,16)
# реальная часть сформированного OFDM символа
plt.figure (3)
plt.plot (t , xt2.real )
n=3
#прием символа на n поднесущей в виде интеграла от
#произведения принятого символа на опорное колебание на n поднесущей
sr=ts=np.sum(xt*np. conjugate(sc_matr[n ,:]) )
#прием символа на Nc поднесущих при помощи ДПФ принятого символа
sr2=np. sqrt (T)/Nc*np.fft.fft (xt) 

plt.show()