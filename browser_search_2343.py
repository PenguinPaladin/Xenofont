# Подключение всех необходимых библиотек
# Нам нужно: speech_recognition, os, sys, webbrowser
# Для первой бибилотеки прописываем также псевдоним
import speech_recognition as sr
import os
import sys
import datetime
from fuzzywuzzy import fuzz
import webbrowser
import pyttsx3
import wikipedia
import re
import requests
import time
import subprocess
from pyowm import OWM
import smtplib
#import urllib
import json
from bs4 import BeautifulSoup
import html2text
#import urllib.request
from urllib import request
from urllib.parse import quote
import lxml
import random
from time import strftime
from urllib.request import urlopen

# настройки
opts = {
    "alias": ('ксенофонт','ксен','ксеноморф','ксенофон','ксенофонт','ксеня',
              'слышь','андроид','дроид','дрон','слушай', 'дубина'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси', 'что такое', 'найди', 'кто такой', 'кто', 'где', 'зачем'),
    "cmds": {
        "ctime": ('текущее время','сейчас времени','который час', 'время', 'времени'),
        "radio": ('включи музыку','воспроизведи радио','включи радио'),
        "stupid1": ('расскажи анекдот','рассмеши меня','ты знаешь анекдоты'),
		"search": ('скажи','покажи','сколько','произнеси', 'что такое', 'найди', 'кто такой', 'кто', 'где', 'зачем'),
    }
}


r = sr.Recognizer()
m = sr.Microphone()


speak_engine = pyttsx3.init()
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[0].id)
# функции
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()

speak("Привет")

def start():
	print("Секунду ...")
	with m as qwerty: r.adjust_for_ambient_noise(qwerty)
	print('говорите')
	r.pause_threshold = 1
	with m as qwerty:
			voice = r.listen(qwerty)
	print("Принял обрабатываю...")
	try:  # Обрабатываем все при помощи исключений
			voice = r.recognize_google(voice, language="ru-RU").lower()
			# Просто отображаем текст что сказал пользователь
			print("Распознано " + voice)
			if 'привет' in voice:
				return command()

			elif '' in voice:
				return start()
	except sr.UnknownValueError:
		# Здесь просто проговариваем слова "Я вас не поняла"
		# и вызываем снова функцию command() для
		# получения текста от пользователя
		voice = start()
	except sr.RequestError as e:
			print("[log] Неизвестная ошибка, проверьте интернет!")
			speak("Неизвестная ошибка, проверьте интернет!")


	return voice



def zapusk(voice):

	if 'привет' in voice:
		return command()

	elif '' in voice:
		return start()


def command():
	# Создаем объект на основе библиотеки
	# speech_recognition и вызываем метод для определения данных

	# Начинаем прослушивать микрофон и записываем данные в source

	print("Секунду ...")
	with m as source: r.adjust_for_ambient_noise(source)
	print("минимум {}".format(r.energy_threshold))
	speak("Чем по́мочь?")
	r.pause_threshold = 1
	with m as source:
		audio = r.listen(source)
	print("Принял обрабатываю...")

	try: # Обрабатываем все при помощи исключений

		zadanie = r.recognize_google(audio, language="ru-RU").lower()
		# Просто отображаем текст что сказал пользователь
		print("Распознано " + zadanie)
		if zadanie.startswith(opts["alias"]):
			cmd = zadanie
			for x in opts['alias']:
				cmd = cmd.replace(x, "").strip()
			for x in opts['tbr']:
				cmd = cmd.replace(x, "").strip()
		# распознаем и выполняем команду
			cmd = recognize_cmd(cmd)
			execute_cmd(cmd['cmd'])

		elif 'найди' in zadanie:
			input = zadanie
			return search(input)

		elif 'расскажи о' in zadanie:
			qet = zadanie
			return search_wiki(qet, headers)

		# Если не смогли распознать текст, то будет вызвана эта ошибка
	except sr.UnknownValueError:
		# Здесь просто проговариваем слова "Я вас не поняла"
		# и вызываем снова функцию command() для
		# получения текста от пользователя
		speak("непонял")
		zadanie = command()
	except sr.RequestError as e:
		print("[log] Неизвестная ошибка, проверьте интернет!")
		speak("Неизвестная ошибка, проверьте интернет!")

	# В конце функции возвращаем текст задания
	# или же повторный вызов функции
	return zadanie





def recognize_cmd(cmd):
	RC = {'cmd': '', 'percent': 0}
	for c, v in opts['cmds'].items():

		for x in v:
			vrt = fuzz.ratio(cmd, x)
			if vrt > RC['percent']:
				RC['cmd'] = c
				RC['percent'] = vrt

	return RC


def execute_cmd(cmd):
	if cmd == 'ctime':
		# сказать текущее время
		now = datetime.datetime.now()
		speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

	elif cmd == 'radio':
		# воспроизвести радио
		os.system("D:\\Jarvis\\res\\radio_record.m3u")

	elif cmd == 'stupid1':
		# рассказать анекдот
		speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")


def search(input):
	reg_ex = re.search('найди (.*)', input.replace('информацию о', '').replace('информацию про', '').replace('про', '').replace('информацию', '').replace('информация о', '').replace('информация о', '').replace('информация про', '').replace('информация', ''))
	url = 'https://ru.wikipedia.org/w/index.php?title='
	if reg_ex:
		zapros = reg_ex.group(1)
		speak('ищю ' + zapros)
		url = url + zapros
		webbrowser.open(url)
		code = requests.get(url)
		soap = BeautifulSoup(code.text, "html.parser")
		text_element = soap.select('p')
		parsed_output = []

		for parse in text_element:
			txt = parse.get_text()
			parsed_output.append(txt)


		print(' '.join(parsed_output).replace('mw-parser-output', ''))
		speak(' '.join(parsed_output).replace('mw-parser-output', ''))

	return command()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.58152',
		   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		   'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}


def search_wiki(qet, headers):
	reg = re.search('расскажи о (.*)', qet)
	url1 = 'https://duckduckgo.com/?q='
	p = '&ia=web'
	#type1 = 'https://api.duckduckgo.com/?q='
	#type2 = '&format=json&pretty=1'
	if reg:
		zapros = reg.group(1)
		poisk = url1 + zapros + p
		webbrowser.open(poisk)
		#json = type1 + zapros + type2
		response = requests.get(poisk, headers=headers)
		soup = BeautifulSoup(response.text, "html.parser")
		#data = response.json
		#all_inf = []
		#all_inf.extend(soup)
		print(soup)
		#speak(data)


	return command()



# Данная функция служит для проверки текста,
# что сказал пользователь (zadanie - текст от пользователя)
def makeSomething(zadanie):
	# Попросту проверяем текст на соответствие
	# Если в тексте что сказал пользователь есть слова
	# "открыть сайт", то выполняем команду

		if zadanie.startswith(opts["alias"]):
			for x in opts['tbr']:
				zadanie = zadanie.replace(x, "").strip()

		elif 'открыть сайт' in zadanie:
			# Проговариваем текст
			speak("открываю")
			# Указываем сайт для открытия
			url = 'https://itproger.com'
			# Открываем сайт
			webbrowser.open(url)
			# если было сказано "стоп", то останавливаем прогу

		elif 'стоп' in zadanie:
			# Проговариваем текст
			speak("Досвидания")
			# Выходим из программы
			sys.exit()
			# Аналогично

		elif 'имя' in zadanie:
			speak("Меня зовут Ксенофонт")

		elif 'привет' in zadanie:
			speak("Доброго времени суток")

		elif 'как дела' in zadanie:
			speak("хорошо")


		elif 'что такое' in zadanie:
			call = zadanie
			if re.search(r'\.', call):
				webbrowser.open_new_tab('https://' + call)
			elif re.search(r'\ ', call):
				webbrowser.open_new_tab('https://yandex.ru/search/?text=' + call)
			else:
				webbrowser.open_new_tab('https://yandex.ru/search/?text=' + call)


		elif 'кто такой' in zadanie:
			call = zadanie
			if re.search(r'\.', call):
				webbrowser.open_new_tab('https://' + call)
			elif re.search(r'\ ', call):
				webbrowser.open_new_tab('https://yandex.ru/search/?text=' + call)
			else:
				webbrowser.open_new_tab('https://yandex.ru/search/?text=' + call)

		elif 'в инете' in zadanie:
			reg_ex = re.search('в инете (.*)', zadanie)
			try:
				if reg_ex:
					look = reg_ex.group(1)
					ny = webbrowser.open_new_tab('https://duckduckgo.com/?q=' + look)
					speak(ny.content[:500].encode('utf-8'))
					webbrowser.open_new_tab(ny.content[:500].encode('utf-8'))
					
			except Exception as e:
				print(e)
				speak(e)

		elif 'фоновoвый режим' in zadanie:
			stop_listening = r.listen_in_background(m, command)


		elif '' in zadanie:
			speak('нет тaкой комады или файла. найти в интернете?')
			print("Секунду ...")
			with m as source:r.adjust_for_ambient_noise(source)
			speak("слушаю")
			r.pause_threshold = 1
			with m as source:
				audio = r.listen(source)
				print("Принял обрабатываю...")
			try:
					otvet = r.recognize_google(audio, language="ru-RU").lower()
					print("Вы сказали " + otvet)
			except sr.UnknownValueError:
				# Здесь просто проговариваем слова "Я вас не поняла"
				# и вызываем снова функцию command() для
				# получения текста от пользователя
				speak("непонял")
				return
			except sr.RequestError as e:
				print("[log] Неизвестная ошибка, проверьте интернет!")
				speak("Неизвестная ошибка, проверьте интернет!")
				return
			if 'да' in otvet:
				speak('ищю ' + (zadanie.replace('найди', '').replace('покажи', '')))
				print('ищю ' + (zadanie.replace('найди', '')))
				webbrowser.open_new_tab('https://duckduckgo.com/?q=' + (zadanie.replace('найди', '').replace('покажи', '')))
			if 'нет' in otvet:
				return command()
			if 'ненадо' in otvet:
				return command()



# Вызов функции для проверки текста будет
# осуществляться постоянно, поэтому здесь
# прописан бесконечный цикл while

while True: makeSomething(command())