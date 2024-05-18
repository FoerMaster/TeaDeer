import ctypes
import win32con
from gui.widgets import MyApp

# Получить дескриптор консоли
console_handle = ctypes.windll.kernel32.GetConsoleWindow()

# Проверить, существует ли консоль
if console_handle:
    # Скрыть консоль
    ctypes.windll.user32.ShowWindow(console_handle, win32con.SW_HIDE)
if __name__ == '__main__':
    MyApp().run()

