import numpy as np
import matplotlib.pyplot as plt

# Открытие файла и чтение данных
file_name = "single_adalm_rx.txt"  # Замените на имя вашего файла
i_values = []
q_values = []

with open(file_name, "r") as file:
    for line in file:
        i, q = map(float, line.strip().split(","))  # Чтение и преобразование строк
        i_values.append(i)
        q_values.append(q)

# Преобразование в массивы numpy
i_values = np.array(i_values)
q_values = np.array(q_values)

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(i_values, label="I (In-phase)", color="blue")
plt.plot(q_values, label="Q (Quadrature)", color="red", linestyle="dashed")

plt.title("График сигналов I и Q")
plt.xlabel("Индекс")
plt.ylabel("Амплитуда")
plt.legend()
plt.grid()
plt.show()

#Для отображения на QPSK созвездие
#plt.figure(figsize=(10, 6))
#plt.scatter(q_values,i_values, color="blue")
#plt.title("График сигналов I и Q")
#plt.grid()
#plt.show()