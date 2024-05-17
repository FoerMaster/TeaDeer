from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.properties import BooleanProperty

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    ''' Добавляет поведение выбора и фокуса к представлению. '''
    selected = BooleanProperty(False)

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Добавляет поддержку выбора к Label. '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Обрабатывает изменения в представлении. '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Добавляет выбор при касании. '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Реагирует на выбор элементов в представлении. '''
        self.selected = is_selected
        if is_selected:
            print(f"Выбран элемент {self.text}")
