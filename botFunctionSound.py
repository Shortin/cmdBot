import telebot
from telebot import types

from config import *
from soundSetting import *

import asyncio
from time import sleep

loop_status = True
id_messange_music = ""
def music_but(message):
    name_track = checkNameTrack()
    status = status_player()
    if(status):
        status = "Плеер запущен"
    else:
        status = "Плеер остановлен"  
        global loop_status
    if(loop_status):
        loop_status = False
        print("loop start")
        asyncio.run(loop_check_name(message))
    bot.send_message(my_chat_id, text = f"Название песни: {name_track[0]}\nИсполнитель: {name_track[1]}\nГромкость: {volume_value()}%\nСтатус: {status}", reply_markup = buttons_music())

@bot.callback_query_handler(func =lambda call: call.data in ['next_track', 'minus_volume', 'start_stop_track', 'plus_volume'])
def inline(call):
    global loop_status
    if(loop_status):
        loop_status = False
        print("loop start")
        asyncio.run(loop_check_name(call.message))
    global id_messange_music
    id_messange_music = call.message.id
    if(call.data == "next_track"):
        music_next()
        music_edit_messange(id_messange_music, 0.750, 0)
    elif(call.data == "minus_volume"):
        volume_sound_decrease(6)
        music_edit_messange(id_messange_music, 0.1, 5)
    elif(call.data == "plus_volume"):
        volume_sound_increase(6)
        music_edit_messange(id_messange_music, 0.1, 5)
    elif(call.data == "start_stop_track"):
        music_play_pause()
        music_edit_messange(id_messange_music, 0, 5)
    try:
    	bot.answer_callback_query(call.id)
    except:
    	print("То ли время истекло, то ли запрос недействителен")

name_track_check = ""
def music_edit_messange(id_messange_music, time_sleep, check):
    try:
        sleep(time_sleep)
        name = checkNameTrack()
        status = status_player()
        if(status):
        	status = "Плеер запущен"
        else:
        	status = "Плеер остановлен"
        global name_track_check
        name_track_check = name[0]+name[1]

        bot.edit_message_text(chat_id=my_chat_id, message_id=id_messange_music, text=f"Название песни: {name[0]} \nИсполнитель: {name[1]} \nГромкость: {volume_value()}%\nСтатус: {status}", reply_markup = buttons_music())
    except:
        if(check >= 5):
        	return
        new_check = check + 1
        music_edit_messange(id_messange_music, time_sleep, new_check)

# В лопере дописать проерку на паузу и настройки звука
async def loop_check_name(message):
    while (1):
        name = checkNameTrack()
        check_name = name[0]+name[1]
        if(name_track_check != check_name):
            id = message.id
            music_edit_messange(id, 0.1, 4)
        else:
            await asyncio.sleep(3)

def buttons_music():
    buttons = types.InlineKeyboardMarkup()
    next_track = types.InlineKeyboardButton("Следующая песня", callback_data = "next_track")
    minus_volume = types.InlineKeyboardButton("-", callback_data = "minus_volume")
    start_stop_track = types.InlineKeyboardButton("старт/стоп", callback_data = "start_stop_track")
    plus_volume = types.InlineKeyboardButton("+", callback_data = "plus_volume")
    buttons.row(next_track)
    buttons.row(minus_volume, start_stop_track, plus_volume)
    return buttons