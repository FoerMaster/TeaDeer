from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from my_kivy_app.screens import MainScreen, AnotherScreen

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AnotherScreen(name='another'))
        return sm

if __name__ == '__main__':
    MyApp().run()
