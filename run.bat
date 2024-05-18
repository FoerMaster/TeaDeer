@echo off
setlocal

REM Установите путь к вашему виртуальному окружению
set VENV_PATH=.venv

REM Проверяем, существует ли виртуальное окружение
if not exist "%VENV_PATH%" (
    echo Виртуальное окружение не найдено: %VENV_PATH%
    goto end
)

REM Устанавливаем переменную среды для Python из виртуального окружения
set PYTHON_EXECUTABLE=%VENV_PATH%\Scripts\python.exe

REM Проверяем, существует ли исполняемый файл Python
if not exist "%PYTHON_EXECUTABLE%" (
    echo Исполняемый файл Python не найден: %PYTHON_EXECUTABLE%
    goto end
)

REM Запускаем main.py без отображения консоли
start /B /MIN %PYTHON_EXECUTABLE% main.py

:end
endlocal