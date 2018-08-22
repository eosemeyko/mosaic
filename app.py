import os
from random import choice
# Для создания GUI
from tkinter import Tk, Label, Frame, Button, PhotoImage
# Для работы с изображениями
from PIL import Image, ImageTk

# Создаём главное окно приложения
main_window = Tk()
# Задаём заголовок окна
main_window.title('Мозаика')

### PARAMS
SIDE = 4  # <- величина стороны квадрата
done_moz_alert = None # Сообщение о том что сборка выполнена
move_count = 0 # Количество перемещений
move_record = 0 # Рекорд по сборке
labels = [] # Массив Label-объектов
### END PARAMS

def key_press(btn, _status=None):
    """ Основная логика перемещения на игровом поле.
        Основной элемент логики - пустая клетка - от неё определяем соседа.
        Потом меняем координаты пустой клетки и соседа.
    """
    near = None

    if btn == 'l' and curr.column > 0:
        # print('Вправо')
        near = label_horizontal(curr)
        curr.column -= 1
        near.column += 1
    elif btn == 'r' and curr.column < SIDE - 1:
        # print('Влево')
        near = label_horizontal(curr, True)
        curr.column += 1
        near.column -= 1
    elif btn == 'd' and curr.row < SIDE - 1:
        # print('Вверх')
        near = label_vertical(curr, True)
        curr.row += 1
        near.row -= 1
    elif btn == 'u' and curr.row > 0:
        # print('Вниз')
        near = label_vertical(curr)
        curr.row -= 1
        near.row += 1

    exchange(curr, near)
    grid_x(curr, near)
    add_count(_status)
    check_done()

def add_count(reset=None):
    """ Создаем счетчик и выводим информацию в окно
    """
    global move_lab, move_count
    if reset == None:
        # Прибавляем к счетчику +1
        move_count += 1
    else:
        move_count = 0
    move_lab['text']= '{}\nMOVE'.format(move_count)

def add_record():
    """ Добавляем числовой рекорд перемещений
    """
    global move_record
    move_record = move_count # Запись рекорда
    record_lab['text'] = '{}\nRecord'.format(move_record) # Вывод сообщения
    add_count(False) # Сброс счетчика

def check_done():
    """
    Проверяем и выводим сообщение что мозаика сложена
    И скрываем ее (если выведена) при изменении
    """
    global done_moz_alert
    # Если состояние мозаики совпадает
    if done_moz == labels:
        # Проверяем на наличие сообщения DONE
        if done_moz_alert == None:
            # Мозайка сложена - Выводим сообщение
            done_moz_alert = Label(main_window, text="DONE!", font=('Courier', 20), foreground="green")
            done_moz_alert.grid(row=3, column=3)
            # Сохраняем рекорд
            add_record()

    else:
        if done_moz_alert: # Если сообщение выведено а мозаика не верно расставлена убираем
            done_moz_alert.destroy()
            done_moz_alert = None

def mix_up():
    """ Перемешивание клеток
    """
    buttons = ['d', 'u', 'l', 'r']
    for _ in range(SIDE ** SIDE):
        x = choice(buttons)
        key_press(x, False)

    # После перешивания делаем сброс счетчика
    add_count(False)

def get_regions(image):
    """ Функция разбиения изображения на квадратики.
        На входе ожидает объект PIL.Image
        Возвращает список картинок-квадратиков ImageTk.PhotoImage
    """
    regions = []
    pixels = image.width // SIDE
    for i in range(SIDE):
        for j in range(SIDE):
            x1 = j * pixels
            y1 = i * pixels
            x2 = j * pixels + pixels
            y2 = i * pixels + pixels
            box = (x1, y1, x2, y2)
            region = image.crop(box)
            region.load()
            regions.append(ImageTk.PhotoImage(region))
    return regions

def make_mosaik_from_filename(filename=''):
    """ Создание мозаики на основе имени файла с картинкой
        Возвращает список картинок-квадратиков ImageTk.PhotoImage
    """
    image = Image.open(filename)
    return get_regions(image)

def generation_image():
    global labels, curr, done_moz
    labels = []
    for i in range(SIDE):
        for j in range(SIDE):
            label = Label(main_window, image=images[i * SIDE + j])
            label.grid(row=i, column=j)
            # задаем новые атрибуты объекту
            label.x = i * SIDE + j
            label.row = i
            label.column = j
            label.count = 0

            labels.append(label)
            # Забираем одну клетку (для курсора)
            curr = labels[-1]
            # Сохраняем растановку мозаики
            done_moz = labels[:]

def label_vertical(curr, up=None):
    """ Вертикальное перемещение
    """
    if up == None:
        row = curr.row - 1
    else:
        row = curr.row + 1
    return labels[row * SIDE + curr.column]

def label_horizontal(curr, left=None):
    """ Горизонтальное перемещение
    """
    if left == None:
        column = curr.column - 1
    else:
        column = curr.column + 1
    return labels[curr.row * SIDE + column]

def grid_x(curr, near):
    """ Отрисовка расположения двух клеток
    """
    if near is not None:
        curr.grid(row=curr.row, column=curr.column)
        near.grid(row=near.row, column=near.column)

def exchange(curr, near):
    """ Обмен местами клеток в общем списке
    """
    if near is not None:
        ci = curr.row * SIDE + curr.column
        ni = near.row * SIDE + near.column
        labels[ci], labels[ni] = labels[ni], labels[ci]

def change_moz_image():
    global images
    # Создание списка картинок мозаики
    images = make_mosaik_from_filename(choice(list_images))
    images[-1] = cubs[-1]
    # Генерируем картинку в поле
    generation_image()
    # Перемешиваем
    mix_up()

# Создаем квадраты мозаики
cubs_count = [os.path.join('assets/cursor.png') for i in range(SIDE ** SIDE)]
cubs = [PhotoImage(file=f) for f in cubs_count]

# Список картинок для мозаики
list_files = os.listdir('img')
list_images = [os.path.join('img', _img_name) for _img_name in list_files]

# Вывод счетчика перемещений справа
move_lab = Label(main_window, width=7, text='0\nMOVE')
move_lab.grid(row=0, column=4, padx=10)

# Вывод счетчика рекорда справа
record_lab = Label(main_window, width=7, text='0\nRECORD')
record_lab.grid(row=1, column=4, padx=10)

# Кнопка перемешивания картинки
reload_img=PhotoImage(file=os.path.join('assets/reload.png'))
btn_reload_img = Button(main_window, image=reload_img, command=mix_up)
btn_reload_img.grid(row=2, column=4)

# Кнопка смены картинки
btn_next_img = Button(
    main_window,
    text="NEXT",
    command=change_moz_image,
    fg="#ccc",
    bg="#555",
    padx="7",
    pady="7",
    font="16")
btn_next_img.grid(row=3, column=4)

# Нажатия стрелок на клавиатуре привызываем к главному окну:
main_window.bind('<Right>', lambda e: key_press('r'))
main_window.bind('<Left>', lambda e: key_press('l'))
main_window.bind('<Up>', lambda e: key_press('u'))
main_window.bind('<Down>', lambda e: key_press('d'))

# Генерируем и перешиваем картинку
change_moz_image()

# Запуск графической оболочки:
main_window.mainloop()