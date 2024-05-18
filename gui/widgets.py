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
import tkinter as tk
from tkinter import filedialog


class MyApp(MDApp):
    def build(self):
        # Устанавливаем полноэкранный режим
        Window.fullscreen = 'auto'

        float_layout = FloatLayout()  # Ограничение размеров
        main_layout = BoxLayout(padding=20, spacing=20)

        # Левый столбец с таблицей
        self.left_column = BoxLayout(orientation='vertical', spacing=10)  # 50% ширины окна

        # Создаем таблицу
        self.table = MDDataTable(
            size_hint=(1, 1),
            column_data=[
                ("Фото-карточки", 100),  # Название и размер столбца "Photo"
                ("Точность", 76)  # Название и размер столбца "Accuracy"
            ],
            elevation=2  # Уровень выносливости
        )
        self.left_column.add_widget(self.table)

        # Добавляем кнопку "Выбрать файл"
        import_button = Button(text='Выбрать файлы (-ы)', size_hint=(1, None), height=40,
                               background_color=(0, 0.5, 1, 1))
        import_button.bind(on_release=self.open_file_chooser)
        self.left_column.add_widget(import_button)

        main_layout.add_widget(self.left_column)

        # Правый столбец с прогресс баром, кнопками и надписью
        right_column = BoxLayout(orientation='vertical', spacing=10)  # 50% ширины окна

        # Добавляем прогресс бар
        progress_bar = MDProgressBar(color=(0.5, 0.5, 0.5, 1), size_hint_y=None, height=dp(6))  # Серый цвет прогресс бара
        right_column.add_widget(progress_bar)

        # Добавляем надпись
        self.preview_label = Label(text='Предпросмотр будет доступен после начала обработки',
                                   size_hint_y=None, height=dp(30), color=(0.5, 0.5, 0.5, 1))  # Серый цвет текста
        right_column.add_widget(self.preview_label)

        # Добавляем кнопку "Обработать"
        process_button = Button(text='Обработать', size_hint_y=None, height=dp(45), background_color=(0, 0.5, 1, 1))
        right_column.add_widget(process_button)

        # Добавляем кнопку "Внести корректировки"
        correction_button = Button(text='Внести корректировки', size_hint_y=None, height=dp(45),
                                   background_color=(0, 0.5, 1, 1))
        right_column.add_widget(correction_button)

        main_layout.add_widget(right_column)

        float_layout.add_widget(main_layout)

        return float_layout

    def open_file_chooser(self, instance):
        chooser = FileChooserIconView()
        popup = Popup(title="Выберите файл",
                      content=chooser,
                      size_hint=(0.9, 0.9))
        chooser.bind(on_selection=lambda x: self._on_file_select(x.selection, popup))
        popup.open()

    def _on_file_select(self, selection, popup):
        if selection:
            for file_path in selection:
                file_name = file_path.split('/')[-1]  # Получаем имя файла
                self.table.row_data.append((file_name, "0%"))  # Добавляем файл в таблицу
            self.table.refresh_rows()  # Обновляем таблицу, чтобы отобразить добавленные файлы
        popup.dismiss()


if __name__ == '__main__':
    MyApp().run()
