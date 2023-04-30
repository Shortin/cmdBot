import telebot
from telebot import types

from config import *
from soundSetting import *

import asyncio
from time import sleep

import logging

loop_status = True # Переменная сообщает о статусе лупера
loop_stop = False # Переменная для остановлки лупера
id_messange_music = "" # Переменная хранит id сообщения с музыкой
name_track_check = "" # Переменная хранит название трека

# Фцнкция status() возвращает статус плеера
# Функция music_but() выводит сообщение с кнопками в телеграмм чате
# Функция music_edit_messange() редактирует сообщение в телеграмм чате
# Функция inline() обрабатывает нажатие инлайн кнопок в телеграмм чате
# Функция loop_check_name() при смене трека обновляет сообщения в телеграмм чате
# Функия buttons_music() возвращает кнопки в сообщение с музыкой

# Фцнкция status() возвращает статус плеера
def status():
    if(status_player()):
        return "Плеер запущен"
    else:
        return "Плеер остановлен"  

# Функция music_but() выводит сообщение с кнопками в телеграмм чате, и запускает функцию loop_check_name()
def music_but(message):
    global loop_stop
    global loop_status
    
    # Переменная для того чтобы остановить лупер
    loop_stop = True
    
    # Проверка на наличие плеера
    if(status_availability_player()):
        bot.send_message(my_chat_id, text = "Плеер не найден")
        return
    
    # Запускает лупер если он не запущен
    if(loop_status):        
        asyncio.run(loop_check_name(message))
        
    # Вывод собщения в чате с кнопками
    name_track = checkNameTrack()
    bot.send_message(my_chat_id, text = f"Название песни: {name_track[0]}\nИсполнитель: {name_track[1]}\nГромкость: {volume_value()}%\nСтатус: {status()}", reply_markup = buttons_music())

# Функция music_edit_messange() редактирует сообщение в телеграмм чате
# Заменяет все данные которые поменялись
def music_edit_messange(id_messange_music, time_sleep, check):
    global name_track_check

    try:
        # Проверяет включен ли плеер
        if(status_availability_player()):
            bot.edit_message_text(chat_id=my_chat_id, message_id=id_messange_music, text=f"Плеер не найден")
            return
        
        # Время для того чтобы успел прогрузиться трек
        sleep(time_sleep)

        # Находит название трека и исполнителя
        name = checkNameTrack()
        name_track_check = name[0]+name[1]

        # Редактирует сообщение в чате телеграмм
        # Заменяет данные которые поменялись
        bot.edit_message_text(chat_id=my_chat_id, message_id=id_messange_music, text=f"Название песни: {name[0]} \nИсполнитель: {name[1]} \nГромкость: {volume_value()}%\nСтатус: {status()}", reply_markup = buttons_music())
    except:
        # Если трек не успел смениться у него есть несколько попыток
        if(check >= 5):
            return
        new_check = check + 1
        music_edit_messange(id_messange_music, time_sleep, new_check)

# Функция inline() обрабатывает нажатие инлайн кнопок в телеграмм чате
# Функция нужна для редактирования данного сообщения
@bot.callback_query_handler(func =lambda call: call.data in ['next_track', 'minus_volume', 'start_stop_track', 'plus_volume'])
def inline(call):
    global loop_status
    global id_messange_music
    
    # Запускает лупер если он не запущен
    if(loop_status):
        asyncio.run(loop_check_name(call.message))
    
    # при нажатии на определенную кнопку выдает определенную команду для редактирования сообщения в телеграмм чате
    id_messange_music = call.message.id
    if(call.data == "next_track"):
        next_track()
        music_edit_messange(id_messange_music, 0.750, 0)
        
    elif(call.data == "minus_volume"):
        volume_sound_setting("-6")
        music_edit_messange(id_messange_music, 0.1, 5)
        
    elif(call.data == "plus_volume"):
        volume_sound_setting("+6")
        music_edit_messange(id_messange_music, 0.1, 5)
        
    elif(call.data == "start_stop_track"):
        music_play_pause()
        music_edit_messange(id_messange_music, 0, 5)
        
    try:
        # метод нужен для правльной работы кнопок в телеграмм чате
        bot.answer_callback_query(call.id)
    except:
        logging.basicConfig(level=logging.error, filename="py_log.log",filemode="a", format="%(asctime)s %(levelname)s %(message)s")
        logging.error("функция inline()(botFunctionSound.py) выдала ошибкy, проблема с обратным запросом инлайн кнопок(bot.answer_callback_query(call.id))")

# Функция loop_check_name() при смене трека обновляет сообщения в телеграмм чате
async def loop_check_name(message):
    global loop_status
    global loop_stop
    global name_track_check
    
    # переменная сообщает о том что запущена функция loop_check_name()
    loop_status = False
    
    # переменная нужна для проверки простоя плеера
    check = 0
    while (1):  
        # При запуске еще одной панели с музыкой останавливается данная функция благодаря переменной loop_stop
        if(loop_stop):
            break
        
        # Проверяем есть ли рабочий плеер, если такого нет то останавливает данную функцию
        if(status_availability_player()):            
            break

        # Проверяем остановлен ли плеер, если да то ведем отсчет 10 минут и останавливаем  функцию
        if(status_player() != True):            
            check += 1
            if(check >= 200):
                break
            music_edit_messange(message.id, 0.1, 4)# Выводит инфу что плеер остановлен
            await asyncio.sleep(3)
            continue
        check = 0
        
        # проверяет сменился ли трек, если да то вызывает функцию которая обновляет информацию в чате телеграмм
        name = checkNameTrack()
        check_name = name[0]+name[1]
        if(name_track_check != check_name):
            music_edit_messange(message.id, 0.1, 4)
        else:
            await asyncio.sleep(3)
    # переменные сообщают о том что остановлена функция loop_check_name()
    loop_status = True
    loop_stop = False

# Функия buttons_music() возвращает кнопки в сообщение с музыкой
def buttons_music():
    buttons = types.InlineKeyboardMarkup()
    next_track = types.InlineKeyboardButton("Следующая песня", callback_data = "next_track")
    minus_volume = types.InlineKeyboardButton("-", callback_data = "minus_volume")
    start_stop_track = types.InlineKeyboardButton("старт/стоп", callback_data = "start_stop_track")
    plus_volume = types.InlineKeyboardButton("+", callback_data = "plus_volume")
    buttons.row(next_track)
    buttons.row(minus_volume, start_stop_track, plus_volume)
    return buttons