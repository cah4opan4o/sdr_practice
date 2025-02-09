import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Открываем файл на чтение
file_name = "D:\\Github\\another task\\sdr\\samples\\data\\txdata.pcm"
# file_name = "D:\\Github\\another task\\sdr\\samples\\data\\txdata_bark.pcm"

# Задаем параметры чтения
dtype = np.int16  # Предполагаем, что данные представлены 16-битными числами
with open(file_name, "rb") as file:
    # Считываем все данные
    data = np.fromfile(file, dtype=dtype)

# Разделяем данные на i и q
i = data[0::2]  # Четные индексы (0, 2, 4, ...)
q = data[1::2]  # Нечетные индексы (1, 3, 5, ...)

# Нормализация данных
i = i / max(abs(i))
q = q / max(abs(q))

# Параметры глазковой диаграммы
symbol_length = 10  # Длина символа (в отсчётах)
num_segments = len(i) // symbol_length  # Количество сегментов для анализа

# Функция для обновления графика глазковой диаграммы
def update(val):
    shift = int(slider.val)  # Получаем текущее значение сдвига
    start = shift  # Начало данных со сдвигом
    end = start + num_segments * symbol_length  # Конец данных для глазковой диаграммы
    i_segmented = i[start:end].reshape(-1, symbol_length)  # Разбиваем на сегменты
    q_segmented = q[start:end].reshape(-1, symbol_length)
    
    # Очищаем текущий график
    ax.clear()
    
    # Построение глазковой диаграммы
    for seg in i_segmented:
        ax.plot(seg, color='blue', alpha=0.7, linewidth=0.5, label="I" if seg is i_segmented[0] else None)
    for seg in q_segmented:
        ax.plot(seg, color='orange', alpha=0.7, linewidth=0.5, label="Q" if seg is q_segmented[0] else None)
    
    # Оформление
    ax.set_title("Глазковая диаграмма")
    ax.set_xlabel("Отсчёты")
    ax.set_ylabel("Амплитуда")
    ax.grid(True)
    ax.legend()
    fig.canvas.draw_idle()  # Перерисовываем график

# Создаем фигуру и оси
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.2)  # Оставляем место для ползунка

# Создаем ползунок
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])  # Позиция и размер ползунка
slider = Slider(ax_slider, 'Сдвиг', 0, symbol_length - 1, valinit=0, valstep=1)  # Ползунок для сдвига (от 0 до длины символа)

# Изначальный график для shift=0
update(0)

# Подключаем функцию обновления к ползунку
slider.on_changed(update)

# Отображаем график
plt.show()
