from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.image import Image, CoreImage
import io
import tkinter as tk
from tkinter import filedialog
from core.model import TeaDeer
from PIL import Image as PImage
from kivy.clock import Clock
from io import BytesIO
import cv2
import threading
import os
import shutil
import userpaths
import random
import string
import subprocess

class MyApp(MDApp):
    def build(self):
        # Устанавливаем полноэкранный режим
        #Window.fullscreen = 'auto'
        self.td = TeaDeer()
        self.td.load('models/640_normal.pt')

        float_layout = FloatLayout()  # Ограничение размеров
        Window.size = (1280, 520)
        self.title = 'TeaDeer - ML/AI сортировщик изображений'
        main_layout = BoxLayout(padding=10, spacing=20)
        self.predicted = 0

        # Левый столбец с таблицей
        self.left_column = BoxLayout(orientation='vertical', spacing=0)  # 50% ширины окна

        # Создаем таблицу
        self.table = MDDataTable(
            size_hint=(1, 1),
            column_data=[
                ("Фото-карточки", dp(80)),  # Название и размер столбца "Photo"
                (" ", dp(30))  # Название и размер столбца "Accuracy"
            ],
            check=False,
            use_pagination=True,
            pagination_menu_height="240dp",
            elevation=0.1
        )
        self.table.bind(on_row_press=self.on_row_press)
        self.left_column.add_widget(self.table)

        # Добавляем кнопку "Выбрать файл"
        import_button = Button(text='Выбрать фотографию', size_hint=(1, None), height=40,
                               background_color=(0, 0.5, 1, 1))
        import_button.bind(on_release=self.open_file_chooser)
        self.left_column.add_widget(import_button)

        import_dir_button = Button(text='Выбрать папку с фотографиями', size_hint=(1, None), height=40,
                               background_color=(0, 0.5, 1, 1))
        import_dir_button.bind(on_release=self.open_file_chooser_dir)
        self.left_column.add_widget(import_dir_button)

        main_layout.add_widget(self.left_column)

        # Правый столбец с прогресс баром, кнопками и надписью
        right_column = BoxLayout(orientation='vertical', spacing=10)  # 50% ширины окна



        f=open("gui/placeholder.jpg",'rb')
        binary_data= f.read() #image opened in binary mode

        data = io.BytesIO(binary_data)
        img = CoreImage(data, ext="png").texture


        self.new_img = Image()
        self.new_img.texture= img
        right_column.add_widget(self.new_img)

        # Добавляем прогресс бар
        self.progress_bar = MDProgressBar(size_hint_y=None, height=dp(10),max = 100, value = 0,type='indeterminate')  # Серый цвет прогресс бара
        right_column.add_widget(self.progress_bar)
        # Добавляем надпись
        self.preview_label = Label(text='Предпросмотр будет доступен после начала обработки',
                                   size_hint_y=None, height=dp(30), color=(0.5, 0.5, 0.5, 1))  # Серый цвет текста
        right_column.add_widget(self.preview_label)

        # Добавляем кнопку "Обработать"
        process_button = Button(text='Начать сортировку всех выбранных изображений', size_hint_y=None, height=dp(45), background_color=(1, 0, 0, 1))
        right_column.add_widget(process_button)
        process_button.bind(on_release=self.start_prediction)

        # # Добавляем кнопку "Внести корректировки"
        # correction_button = Button(text='Внести корректировки', size_hint_y=None, height=dp(45),
        #                            background_color=(0, 0.5, 1, 1))
        # right_column.add_widget(correction_button)

        main_layout.add_widget(right_column)

        float_layout.add_widget(main_layout)

        return float_layout
    def on_row_press(self,  table, row):
        # get start index from selected row item range
        start_index, end_index = row.table.recycle_data[row.index]["range"]
        try:
            # Добавляем прогресс бар
            f=open(row.table.recycle_data[end_index-1]["text"],'rb')
            binary_data= f.read() #image opened in binary mode

            data = io.BytesIO(binary_data)
            img = CoreImage(data, ext="png").texture
            self.new_img.texture= img
        except:
            print("Cant load image...")

    def start_prediction(self, instance):
        # Create a new thread and start it
        prediction_thread = threading.Thread(target=self._start_prediction_thread)
        prediction_thread.start()

    def collect_images(self, directory):
        image_array = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(root, file)
                    image_array.append(image_path)
        return image_array

    def _start_prediction_thread(self):
        self.preview_label.text = 'Загружаем модель...'
        self.progress_bar.color = (0.1,0.1,0.5,1)
        self.predicted = 0
        total_rows = len(self.table.row_data)
        my_docs = userpaths.get_my_documents()
        os.makedirs(my_docs+'/TeaDeer', exist_ok=True)
        os.makedirs(my_docs+'/Обработанные фото', exist_ok=True)
        os.makedirs(my_docs+'/Обработанные фото/Кабарги', exist_ok=True)
        os.makedirs(my_docs+'/Обработанные фото/Олени', exist_ok=True)
        os.makedirs(my_docs+'/Обработанные фото/Косули', exist_ok=True)
        for row in self.table.row_data:
            results = self.td.model.predict(row[0], conf=0.3, stream=True)
            for r in results:
                # Assuming r.plot() returns an image in BGR color space
                im_bgr = r.plot()
                # Convert the image from BGR to RGB color space
                im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)

                # Create a PIL Image from the RGB image
                pil_image = PImage.fromarray(im_rgb)

                # Save the PIL Image to a BytesIO object in PNG format
                img_bytes = BytesIO()
                pil_image.save(img_bytes, format='PNG')

                # Reset the BytesIO object to the start
                img_bytes.seek(0)

                # Create a Kivy CoreImage from the BytesIO object
                img = CoreImage(img_bytes, ext="png")

                # Update the image texture on the main thread
                Clock.schedule_once(lambda dt, ti=img: self._update_image(ti))

                # Update the progress bar on the main thread
                self.predicted += 1
                progress = (self.predicted / total_rows) * 100
                Clock.schedule_once(lambda dt, p=progress: self._update_progress(p))
                if len(r.boxes.cls) > 0:
                    dear_class = int(r.boxes.cls[0])
                    if dear_class == 0:
                        shutil.copy(r.path, my_docs+'/Обработанные фото/Олени')
                    elif dear_class == 1:
                        shutil.copy(r.path, my_docs+'/Обработанные фото/Кабарги')
                    elif dear_class == 2:
                        shutil.copy(r.path, my_docs+'/Обработанные фото/Косули')
                else:
                    shutil.copy(r.path, my_docs+'/Обработанные фото/Не распознанно')

        random_chars = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
        self.td.compress(my_docs+'/Обработанные фото',my_docs+'/TeaDeer/dat_'+random_chars)
        openPath = f"{my_docs}\\TeaDeer\\dat_{random_chars}.zip"
        os.system(f"explorer.exe /select,{openPath}")
        self.preview_label.text = 'Готово!, Архив на вашем рабочем столе!'
        self.progress_bar.color = (0,1,0,1)
        self.table.row_data = []
        shutil.rmtree(my_docs+'/Обработанные фото')

    def _update_image(self, img):
        self.new_img.texture = img.texture

    def open_file_chooser(self, instance):
        root = tk.Tk()
        root.withdraw()
        for path in filedialog.askopenfiles(filetypes=[("Фотокарточки", ".jpg .jpeg .png")]):
            self.table.row_data.append([path.name," "])
        return( )

    def open_file_chooser_dir(self, instance):
        root = tk.Tk()
        root.withdraw()
        dir = filedialog.askdirectory()
        images = self.collect_images(dir)
        for image in images:
            self.table.row_data.append([image," "])

        # chooser = FileChooserIconView()
        # popup = Popup(title="Выберите файл",
        #               content=chooser,
        #               size_hint=(0.9, 0.9))
        # chooser.bind(on_selection=lambda x: self._on_file_select(x.selection, popup))
        # popup.open()
    def _update_progress(self, progress):
        self.progress_bar.value = progress
        self.preview_label.text = f"Обработка, завершено {round(progress)}%"
    def _on_file_select(self, selection, popup):
        if selection:
            for file_path in selection:
                file_name = file_path.split('/')[-1]  # Получаем имя файла
                self.table.row_data.append((file_name, "0%"))  # Добавляем файл в таблицу
            self.table.refresh_rows()  # Обновляем таблицу, чтобы отобразить добавленные файлы
        popup.dismiss()


if __name__ == '__main__':
    MyApp().run()
