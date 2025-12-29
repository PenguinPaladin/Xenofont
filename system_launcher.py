import subprocess
import sys
import os

# Конфигурация: голосовая команда -> путь/команда для запуска
PROGRAM_MAP = {
    # Windows examples
    "блокнот": "notepad.exe",
    "калькулятор": "calc.exe",
    "браузер": r"C:\Program Files\Firefox\firefox.exe",
    # Linux examples
    "текстовый редактор": "gedit",
    "терминал": "gnome-terminal",
}

def launch_program(app_name):
    """
    Запускает программу по ее голосовому имени.
    Возвращает строку-результат для озвучивания.
    """
    # Ищем ключ в конфиге (регистронезависимо)
    for key, command in PROGRAM_MAP.items():
        if key in app_name.lower():
            try:
                # Запускаем в отдельном процессе, НЕ дожидаясь завершения (shell=False для безопасности)
                if sys.platform == "win32":
                    subprocess.Popen(command, shell=False)
                else:
                    subprocess.Popen(command.split(), shell=False)
                return f"Запускаю {key}"
            except FileNotFoundError:
                return f"Не найден файл для {key}"
            except Exception as e:
                return f"Ошибка при запуске: {e}"
    return f"Не знаю, как запустить '{app_name}'. Вы можете добавить эту программу в конфигурацию."