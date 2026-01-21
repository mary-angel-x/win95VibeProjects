import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(BASE_DIR, "img")




class WebPunkObject:
    def __init__(self,canvas,screen_width,screen_height):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height
    def update(self):
        pass

class MatrixDropObject(WebPunkObject):
    def __init__(self,canvas,screen_width,screen_height,font_size,x,chars,color):
        super().__init__(canvas,screen_width,screen_height)
        self.font_size = font_size
        self.chars = chars
        self.color = color
        self.coords = []
        self.char_obj_id = self.canvas.create_text(x, random.randint(-600, 0),
                                               text=random.choice(self.chars),
                                               fill=color, font=("Fixedsys", self.font_size))

    def update(self):
        # 1. Движение вниз
        self.canvas.move(self.char_obj_id, 0, 7) #

        # 2. Получение координат
        self.coords = self.canvas.coords(self.char_obj_id)

        # 3. Проверка границы и возврат наверх
        if self.coords[1] > self.screen_height:
            self.canvas.coords(self.char_obj_id, self.coords[0], random.randint(-100, 0))

        # 4. Обновление текста
        self.canvas.itemconfig(self.char_obj_id, text=random.choice(self.chars))


class GifObject(WebPunkObject):
    def __init__(self, canvas, screen_width, screen_height, file_name, x, y):
        super().__init__(canvas, screen_width, screen_height)

        # 1. Путь к файлу
        file_path = os.path.join(img_dir, file_name)

        try:
            # 2. Загрузка кадров прямо в объект
            pil_img = Image.open(file_path)
            self.frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA"))
                           for frame in ImageSequence.Iterator(pil_img)]

            self.current_frame = 0  # У каждого объекта свой счетчик

            # 3. Создаем картинку на холсте и сохраняем ID
            self.id = self.canvas.create_image(x, y, image=self.frames[0], anchor="nw")

        except Exception as e:
            print(f"Ошибка загрузки GIF {file_name}: {e}")
            self.id = None

    def update(self):
        # Если загрузка не удалась, ничего не делаем
        if not self.id: return

        # 1. Меняем индекс кадра
        self.current_frame = (self.current_frame + 1) % len(self.frames)

        # 2. Обновляем картинку на холсте по ID
        self.canvas.itemconfig(self.id, image=self.frames[self.current_frame])

class NeonTextObject(WebPunkObject):
    def __init__(self, canvas, width, height, text, x, y, palette): # palette - это вход
        super().__init__(canvas, width, height)
        self.colors = palette  # Сохранили то, что нам дали
        self.id = self.canvas.create_text(x, y, text=text, fill=self.colors[0], font=("Fixedsys", 40))

    def update(self):
        # Используем то, что нам дали при создании
        self.canvas.itemconfig(self.id, fill=random.choice(self.colors))


class WebPunkApp:
    def __init__(self, root):
        self.root = root
        # 1. Настройки окна
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, highlightthickness=0)
        self.canvas.pack()


        try:
            path = os.path.join(img_dir, "back.jpg")
            img = Image.open(path).resize((self.width, self.height))
            self.bg_img = ImageTk.PhotoImage(img)

            # Рисуем на холсте (0,0 - левый верхний угол)
            self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        except Exception as e:
            print(f"Фон не найден: {e}")
            self.canvas.config(bg="#008080")  # Цвет Win95 если картинки нет


        # 2. Список для ВСЕХ объектов (полиморфизм)
        self.objects = []

        # 3. СОЗДАНИЕ ОБЪЕКТОВ
        # Здесь ТЫ задаешь параметры (символы, цвета, координаты)

        # Создаем капли (Слой 1)
        matrix_symbols = "ｦｱｳｴｵ123456789010101010101010110101010110101010110"
        for x in range(0, self.width, 10):
            # Передаем в объект всё: канвас, размеры экрана и символы
            drop = MatrixDropObject(self.canvas, self.width, self.height, 20, x, matrix_symbols,'#8B00FF')
            self.objects.append(drop)

        # Добавляем гифку (Слой 2)

        self.objects.append(GifObject(self.canvas, self.width, self.height, 'load.gif', 150, 300))
        self.objects.append(GifObject(self.canvas, self.width, self.height, 'win95.gif', 0, 0))
        self.objects.append(GifObject(self.canvas, self.width, self.height, 'smp.gif', 300, -150))

        # Добавляем неоновый текст с ТВОИМИ цветами (Слой 3)
        my_colors = ["#FF00FF", "#00FFFF", "#FFFFFF"]
        self.objects.append(NeonTextObject(self.canvas, self.width, self.height, "SYSTEM ERROR", 400, 200, my_colors))

        # 4. Запуск цикла
        self.run()

    def run(self):
        # ОДИН цикл для всего
        for obj in self.objects:
            obj.update()  # Капля падает, гифка крутится, текст мигает

        # Повтор через 50 мс
        self.root.after(50, self.run)

if __name__ == "__main__":
    root = tk.Tk()
    app = WebPunkApp(root)
    root.mainloop()