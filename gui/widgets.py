from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle, Color

from gui.screens import MainScreen

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': f'Элемент {i+1}'} for i in range(5)]

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))

        # Создание основного GridLayout с двумя столбцами
        main_grid = GridLayout(cols=2, padding=10, spacing=10)

        # Создание RecycleView слева
        rv = RV()

        # Создание вложенного GridLayout для списка и кнопки
        list_layout = GridLayout(cols=1, spacing=10)
        list_layout.add_widget(rv)

        # Добавление границы к list_layout
        with list_layout.canvas.before:
            Color(210/255, 210/255, 210/255, 1)  # Цвет границы (светло-серый)
            self.rect = Rectangle(size=list_layout.size, pos=list_layout.pos)
        list_layout.bind(pos=self.update_rect, size=self.update_rect)

        # Изменение размера кнопки и распределение ширины
        button = Button(
            text='Импортировать файл',
            size_hint_x=1,
            size_hint_y=None,
            height=50)
        list_layout.add_widget(button)

        # Добавление отступа между кнопкой и списком
        list_layout.spacing = 10

        # Добавление list_layout в левый столбец основного grid
        main_grid.add_widget(list_layout)

        # Создание правого GridLayout для инпутов и кнопки
        right_grid = GridLayout(cols=1, spacing=10)

        # Создание вложенного GridLayout для двух TextInput
        input_grid = GridLayout(cols=1, spacing=10)

        # Создание двух TextInput в верхней части правого грида с плейсхолдерами
        input1 = TextInput(hint_text='Порог срабатывания', size_hint_y=None, height=50, multiline=False)
        input2 = TextInput(hint_text='...', size_hint_y=None, height=50, multiline=False)

        # Добавление TextInput в input_grid
        input_grid.add_widget(input1)
        input_grid.add_widget(input2)

        # Добавление кнопки "Обработка" внизу правого грида
        processing_button = Button(
            text='Обработка',
            size_hint_y=None,
            height=50)

        # Добавление input_grid и processing_button в right_grid
        right_grid.add_widget(input_grid)
        right_grid.add_widget(processing_button)

        # Добавление правого грида в правый столбец основного grid
        main_grid.add_widget(right_grid)

        return main_grid

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
