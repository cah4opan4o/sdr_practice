import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Открываем файл на чтение
file_name = "/home/plutosdr/Desktop/ia232/sdr/test1/sdrLessons/build/txdata_bark.pcm"
# file_name = "/home/plutosdr/Desktop/ia232/sdr/samples/data/txdata123.pcm"
# file_name = "D:\\Github\\another task\\sdr\\samples\\data\\txdata_bark.pcm"

# Задаем параметры чтения
dtype = np.int16  # Предполагаем, что данные представлены 16-битными числами
with open(file_name, "rb") as file:
    # Считываем все данные
    data = np.fromfile(file, dtype=dtype)

# Разделяем данные на i и q
i = data[0::2]
q = data[1::2]

i_ = i
q_ = q

# Нормализация данных
i = i / max(abs(i))
q = q / max(abs(q))


filter = np.ones(10)
i = np.convolve(i,filter,mode='same')
q = np.convolve(q,filter,mode='same')



plt.figure(1)
plt.plot(i)
plt.plot(q)
plt.plot(i_,color = "green")
plt.plot(q_,color = "purple")

count = 0
plt.figure(2, figsize=(16,16))
for it in range(1,11):
    i_new = i[it::10]
    q_new = q[it::10]
    count += 1
    plt.subplot(2,5,count)
    # plt.scatter(q_new,i_new)
    plt.grid(True)
    plt.plot(q_new)
    plt.plot(i_new)


# Функция для обновления графика созвездия
def update(val):
    shift = int(slider.val)  # Получаем текущее значение сдвига
    i_shifted = i[shift::10]  # Берем каждый 10-й элемент с учетом сдвига
    q_shifted = q[shift::10]
    
    # Обновляем данные графика
    scatter.set_offsets(np.c_[q_shifted,i_shifted])  # np.c_ объединяет i и q в двумерный массив
    fig.canvas.draw_idle()  # Перерисовываем график

# Создаем фигуру и оси
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.2)  # Оставляем место для ползунка

# Изначальный график для shift=0
i_shifted = i[0::10]
q_shifted = q[0::10]
scatter = ax.scatter(q_shifted,i_shifted, s=1, alpha=0.7)

# Настройка осей
ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)
ax.axvline(0, color='gray', linestyle='--', linewidth=0.5)
ax.set_title("Созвездие QPSK с изменяемым сдвигом")
ax.set_ylabel("I (In-Phase)")
ax.set_xlabel("Q (Quadrature)")
ax.grid(True)
ax.axis('equal')

# Создаем ползунок
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])  # Позиция и размер ползунка
slider = Slider(ax_slider, 'Сдвиг', 0, 9, valinit=0, valstep=1)  # Ползунок для сдвига (от 0 до 9)

# Подключаем функцию обновления к ползунку
slider.on_changed(update)

# Отображаем график
plt.show()
