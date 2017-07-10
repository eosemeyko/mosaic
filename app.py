# Подключение модулей
import os
from tkinter import * # Модуль tkinter - для создания GUI
from random import choice

# PEP 8
# Для работы с графикой воспользуемся дополнительной библиотекой - PIL
# Необходимо установить библиотеку Pillow:  pip install Pillow
from PIL import Image, ImageTk

# Создаём главное окно приложения
main_window = Tk()
# Задаём заголовок окна
main_window.title('Мозаика')

### PARAMS
SIDE = 4  # <- величина стороны квадрата (для пятнашек квадрат 4х4)
done_moz_alert = None
#btn_change_img = None
record = None # Рекорд по сборке
labels = [] # Создание и размещение Label-объектов
### END PARAMS

# Выводим счетчик справа
move_lab = Label(main_window, width=7, text='0\nMOVE')
move_lab.grid(row=0, column=4, padx=10)

# Вывод сообщения рекорда
record_lab = Label(main_window, width=7, text='0\nRECORD')
record_lab.grid(row=1, column=4, padx=10)

def key_press(btn, _status=None):
    """ Основная логика перемещения на игровом поле.
        Основной элемент логики - пустая клетка - от неё определяем соседа.
        Потом меняем координаты пустой клетки и соседа.
    """
    near = None

    if btn == 'l' and curr.column > 0:
        # print('Вправо')
        near = label_left(curr)
        curr.column -= 1
        near.column += 1
    elif btn == 'r' and curr.column < SIDE - 1:
        # print('Влево')
        near = label_right(curr)
        curr.column += 1
        near.column -= 1
    elif btn == 'd' and curr.row < SIDE - 1:
        # print('Вверх')
        near = label_under(curr)
        curr.row += 1
        near.row -= 1
    elif btn == 'u' and curr.row > 0:
        # print('Вниз')
        near = label_above(curr)
        curr.row -= 1
        near.row += 1

    exchange(curr, near)
    grid_x(curr, near)
    check_count(curr, _status)
    check_done(curr, _status)


def check_count(curr, _status):
    """ Создаем счетчик и выводим информацию в окно
    """
    global move_lab
    if _status == None:
        # Прибавляем к счетчику +1
        curr.count += 1
        move_lab['text']= '{}\nMOVE'.format(curr.count)


def check_done(curr, _status):
    """
    Проверяем и выводим сообщение что мозаика сложена
    И скрываем ее (если выведена) при изменении
    """
    global done_moz_alert, record
    # Если состояние мозаики совпадает
    if done_moz == labels:
        # Проверяем на наличие сообщения DONE
        if done_moz_alert == None:
            # Мозайка сложена - Выводим сообщение
            done_moz_alert = Label(main_window, text="DONE!", font=('Courier', 20), foreground="green")
            done_moz_alert.grid(row=3, column=3)
            # Выводим кнопку для обновления картинки
            # btn_change_img = Button(main_window, text="NEXT", fg="green", command=change_moz_image)
            # btn_change_img.grid(row=3, column=4)

            record = curr.count # Запись рекорда
            curr.count = 0 # Сброс счетчика
            record_lab['text'] = '{}\nRecord'.format(record)

    else:
        if done_moz_alert: # Если сообщение выведено а мозаика не верно расставлена убираем
            done_moz_alert.destroy()
            done_moz_alert = None
            #btn_change_img.destroy()


def mix_up():
    """ Перемешивание клеток
        SIDE ** 4 - взято для лучшего перемешивания,
         т.к. не все вызовы функции нажатия кнопок
         будут приводить клеток к движению на поле
    """
    buttons = ['d', 'u', 'l', 'r']
    for i in range(SIDE ** 4):
        x = choice(buttons)  # <- choice - функция из модуля random
        key_press(x, 'false')

    # После перешивания делаем сброс счетчика
    curr.count = 0

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

# список файлов в папке
images_list = os.listdir('nums')
num_files = [os.path.join('nums', _img_name) for _img_name in images_list]

# Список объектов-картинок с числами:
nums = [PhotoImage(file=f) for f in num_files]

# Список картинок для мозаики
images_list2 = os.listdir('img')
list_files = [os.path.join('img', _img_name2) for _img_name2 in images_list2]

# Создание списка картинок мозаики
images = make_mosaik_from_filename(choice(list_files))
images[-1] = nums[-1]

def generation_image():
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

generation_image()
curr = labels[-1]

# Сохраняем растановку мозаики
done_moz = labels[:]

def label_above(curr):
    """ Вернуть соседа сверху
    """
    return labels[(curr.row - 1) * SIDE + curr.column]


def label_under(curr):
    """ Вернуть соседа снизу
    """
    return labels[(curr.row + 1) * SIDE + curr.column]


def label_left(curr):
    """ Вернуть соседа слева
    """
    return labels[curr.row * SIDE + curr.column - 1]


def label_right(curr):
    """ Вернуть соседа справа
    """
    return labels[curr.row * SIDE + curr.column + 1]


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
    images = make_mosaik_from_filename(choice(list_files))
    images[-1] = nums[-1]
    # Генерируем картинку в поле
    #generation_image()
    # Перемешиваем
    mix_up()

btn_change_img = Button(main_window, text="NEXT", fg="green", command=change_moz_image)
btn_change_img.grid(row=3, column=4)

# Нажатия стрелок на клавиатуре привызываем к главному окну:
main_window.bind('<Right>', lambda e: key_press('r'))
main_window.bind('<Left>', lambda e: key_press('l'))
main_window.bind('<Up>', lambda e: key_press('u'))
main_window.bind('<Down>', lambda e: key_press('d'))

mix_up()


# Запуск главного цикла обработки сообщений графической оболочки:
main_window.mainloop()