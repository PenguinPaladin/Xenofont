import speech_recognition as sr
import datetime
import webbrowser
import requests
import time
import random
import os
from urllib.parse import quote
from gtts import gTTS
import playsound3 as playsound

# Инициализация
r = sr.Recognizer()
m = sr.Microphone()

# Функция для озвучивания текста
def speak(text):
    print(f"Ассистент: {text}")
    try:
        tts = gTTS(text=text, lang='ru')
        filename = "temp_speech.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    except Exception as e:
        print(f"Ошибка озвучки: {e}")

# Слушаем команду
def listen_command():
    try:
        with m as source:
            print(">>> Слушаю...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        try:
            command = r.recognize_google(audio, language="ru-RU").lower()
            print(f"Вы сказали: {command}")
            return command
        except sr.UnknownValueError:
            speak("Я вас не понял")
            return None
        except sr.RequestError:
            speak("Ошибка соединения")
            return None
    except sr.WaitTimeoutError:
        speak("Я вас не услышал")
        return None

# Обработка команд
def process_command(command):
    if not command:
        return False
    
    # Команды выхода
    if any(word in command for word in ['стоп', 'выход', 'пока', 'до свидания']):
        speak("До свидания! Рад был помочь")
        return True
    
    # Обычные команды
    elif 'привет' in command:
        speak("Привет! Чем могу помочь?")
        
    elif 'как дела' in command or 'как ты' in command:
        responses = [
            "У меня всё отлично, спасибо что спросили!",
            "Работаю в штатном режиме!",
            "Всё хорошо, готов помогать!"
        ]
        speak(random.choice(responses))
        
    elif 'время' in command or 'который час' in command:
        now = datetime.datetime.now()
        speak(f"Сейчас {now.hour} часов {now.minute} минут")
        
    elif 'найди' in command or 'ищи' in command or 'поиск' in command:
        if 'найди' in command:
            query = command.replace('найди', '').strip()
        elif 'ищи' in command:
            query = command.replace('ищи', '').strip()
        else:
            query = command.replace('поиск', '').strip()
            
        if query:
            speak(f"Ищу информацию о {query}")
            url = f'https://ru.wikipedia.org/wiki/{quote(query)}'
            webbrowser.open(url)
            time.sleep(0.5)
            speak("Открываю результаты поиска")
        else:
            speak("Что именно вы хотите найти?")
            
    elif 'открой браузер' in command or 'браузер' in command:
        speak("Открываю браузер")
        webbrowser.open("https://www.google.com")
        
    elif 'включи музыку' in command or 'музыку' in command or 'радио' in command:
        speak("Включаю музыку")
        webbrowser.open("https://www.youtube.com")
        
    elif 'анекдот' in command or 'шутку' in command or 'рассмеши' in command:
        jokes = [
            "Почему программист всегда мокрый? Потому что он постоянно в бассейне с кодом!",
            "Какой язык программирования самый романтичный? Java, потому что у него всегда есть кофе!",
            "Почему Python не хочет идти на вечеринку? Потому что у него слишком много скобок!"
        ]
        speak(random.choice(jokes))
        
    elif 'спасибо' in command:
        speak("Всегда пожалуйста!")
        
    elif 'имя' in command or 'зовут' in command:
        speak("Меня зовут Ксенофонт")
        
    else:
        speak("Извините, я не понял команду. Попробуйте сказать 'найди', 'время' или 'открой браузер'")
    
    return False

# Главная функция
def main():
    speak("Привет! Я голосовой помощник Ксенофонт.")
    time.sleep(1)
    speak("Готов к работе! Скажите что-нибудь.")
    
    # Главный цикл
    while True:
        try:
            # Слушаем команду
            command = listen_command()
            
            if command:
                should_exit = process_command(command)
                if should_exit:
                    break
            
        except KeyboardInterrupt:
            speak("Завершаю работу")
            break
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(2)

# Запуск программы
if __name__ == "__main__":
    main()