import numpy as np
import matplotlib.pyplot as plt

# Открываем файл на чтение
file_name = "D:\\Github\\another task\\sdr\\samples\\data\\txdata123.pcm"
# file_name = "D:\\Github\\another task\\sdr\\samples\\data\\txdata_bark.pcm"
dtype = np.int16
with open(file_name, "rb") as file:
    data = np.fromfile(file, dtype=dtype)

i = data[0::2]
q = data[1::2]

# Это делается для приведения данных к стандартному масштабу, например, от -1 до 1
i = i / max(abs(i))
q = q / max(abs(q))

# Выводим график
plt.figure(figsize=(10, 6))
plt.plot(i, label="I")
plt.plot(q, label="Q")

plt.title("График данных I и Q")
plt.xlabel("Индекс")
plt.ylabel("Амплитуда")
plt.legend()
plt.grid(True)


fig, axes = plt.subplots(5, 2, figsize=(15, 10))  # 5 строк, 2 столбца
axes = axes.ravel()  # Преобразуем массив осей в одномерный для удобства

# Построение 10 графиков
for shift in range(10):
    i_shifted = i[shift::10]
    q_shifted = q[shift::10]
    
    # Выбираем текущий subplot
    ax = axes[shift]
    ax.plot(i_shifted, label=f"I (сдвиг {shift})")
    ax.plot(q_shifted, label=f"Q (сдвиг {shift})")
    
    ax.set_title(f"График каждых 10-х данных (сдвиг {shift})")
    ax.set_xlabel("Индекс")
    ax.set_ylabel("Амплитуда")
    ax.legend()
    ax.grid(True)

# Добавляем отступы между графиками
plt.tight_layout()



# Построение созвездия QPSK
plt.figure(figsize=(8, 8))
plt.scatter(i, q, s=1, alpha=0.7)  # s=1 уменьшает размер точек, alpha=0.7 делает их полупрозрачными
plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
plt.axvline(0, color='gray', linestyle='--', linewidth=0.5)
plt.title("Созвездие QPSK")
plt.xlabel("I (In-Phase)")
plt.ylabel("Q (Quadrature)")
plt.grid(True)
plt.axis('equal')  # Сохраняем одинаковый масштаб по осям
plt.show()

# Отображаем график
plt.show()
