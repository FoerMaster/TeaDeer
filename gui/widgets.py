from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from gui.screens import MainScreen

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': f'Элемент {i + 1}'} for i in range(5)]

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_color_normal = (0 / 255, 130 / 255, 255 / 255, 1)  # Стандартный цвет кнопки (hex #0082ff)
        self.background_color_down = (0 / 255, 110 / 255, 255 / 255, 1)  # Цвет кнопки при нажатии (hex #006eff)
        self.background_color = self.background_color_normal  # Изначально устанавливаем стандартный цвет кнопки
        self.bind(on_state=self.update_color)  # Обновляем цвет при изменении состояния

    def update_color(self, instance, value):
        # Обновляем цвет кнопки в зависимости от состояния
        if value == 'down' or self.focus:
            self.background_color = self.background_color_down
        else:
            self.background_color = self.background_color_normal

class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super(CustomTextInput, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)  # Белый фон
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.border_color = Color(0, 0, 0, 1)  # Черная рамка
            self.border_line = Line(rectangle=(self.x, self.y, self.width, self.height), width=1)
        self.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

    def _update_bg_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
        self.border_line.rectangle = (self.x, self.y, self.width, self.height)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        Window.clearcolor = (1, 1, 1, 1)

        main_grid = GridLayout(cols=2, padding=(20, 20), spacing=20)

        rv = RV()

        list_layout = GridLayout(cols=1, spacing=10)
        list_layout.add_widget(rv)

        with list_layout.canvas.before:
            Color(240 / 255, 240 / 255, 240 / 255, 1)
            self.rect = Rectangle(size=list_layout.size, pos=list_layout.pos)
        list_layout.bind(pos=self.update_rect, size=self.update_rect)

        main_grid.add_widget(list_layout)

        right_grid = BoxLayout(orientation='vertical', spacing=10, padding=[0, 0, 0, 20])

        input_grid = GridLayout(cols=2, spacing=10, row_force_default=True, row_default_height=50)

        input1 = CustomTextInput(hint_text='', multiline=False)
        input2 = CustomTextInput(hint_text='', multiline=False)

        label1 = Label(text='Порог срабатывания', color=(0, 0, 0, 1), size_hint_x=None, width=300, halign='left', valign='middle')
        label2 = Label(text='Разрешение фото', color=(0, 0, 0, 1), size_hint_x=None, width=300, halign='left', valign='middle')

        label1.bind(size=label1.setter('text_size'))
        label2.bind(size=label2.setter('text_size'))

        input_grid.add_widget(label1)
        input_grid.add_widget(input1)
        input_grid.add_widget(label2)
        input_grid.add_widget(input2)

        right_grid.add_widget(input_grid)

        button_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=60)

        processing_button = RoundedButton(
            text='Обработать',
            size_hint_y=None,
            height=60,
        )
        processing_button.bind(on_press=lambda x: setattr(x, 'state', 'down'))
        processing_button.bind(on_release=lambda x: setattr(x, 'state', 'normal'))

        import_button = RoundedButton(
            text='Импортировать файл (-ы)',
            size_hint_y=None,
            height=60,
        )
        import_button.bind(on_press=lambda x: setattr(x, 'state', 'down'))
        import_button.bind(on_release=lambda x: setattr(x, 'state', 'normal'))
        import_button.bind(on_release=self.open_file_chooser)

        button_layout.add_widget(processing_button)
        button_layout.add_widget(import_button)

        right_grid.add_widget(BoxLayout(size_hint_y=1))  # Добавляем растягивающий виджет перед кнопками, чтобы опустить их вниз
        right_grid.add_widget(button_layout)

        main_grid.add_widget(right_grid)

        return main_grid

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def open_file_chooser(self, instance):
        filechooser = FileChooserIconView()
        popup = Popup(title="Выберите файл",
                      content=filechooser,
                      size_hint=(0.9, 0.9))
        filechooser.bind(on_selection=lambda x: self._on_file_select(x.selection, popup))
        popup.open()

    def _on_file_select(self, selection, popup):
        if selection:
            print(f'File selected: {selection[0]}')
        popup.dismiss()

if __name__ == '__main__':
    MyApp().run()
