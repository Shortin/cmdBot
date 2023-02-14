import telebot
from telebot import types

from config import *

from botFunctionSound import music_but
from soundSetting import volume_sound_expose, volume_sound_decrease, volume_sound_increase
from function import *

# При удалении сообщения пропадают кнопки надо фиксить
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(my_chat_id, text = "Что-то хотели?", reply_markup = buttons_menu())

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.chat.id != my_chat_id):
        return

    if(message.text == "музыка" or message.text == "music"):
        music_but(message)

    elif(message.text == "ssh" or message.text == "ссш"):
        bot.send_message(my_chat_id, text = "кнопки", reply_markup = buttons_ssh())
    elif(message.text == "xrdp" or message.text == "хрдп"):
        bot.send_message(my_chat_id, text = "кнопки", reply_markup = buttons_xrdp())
    elif(message.text == "экран" or message.text == "screen"):
        bot.send_message(my_chat_id, text = "кнопки", reply_markup = buttons_screen())
    elif(message.text == "громкость" or message.text == "volume"):
        bot.send_message(my_chat_id, text = "кнопки", reply_markup = buttons_volume())

    elif(message.text == "назад" or message.text == "back"):
        bot.send_message(my_chat_id, text = "Что-то хотели?", reply_markup = buttons_menu())

    elif(message.text == "ip" or message.text == "ип"):
        bot.send_message(my_chat_id, text = get_external_ip())


    elif(message.text == "-"):
        bot.delete_message(my_chat_id, message.message_id)
        volume_sound_decrease(6)
    elif(message.text == "+"):
        bot.delete_message(my_chat_id, message.message_id)
        volume_sound_increase(6)

    elif(message.text == "value" or message.text == "значение"):
        bot.send_message(my_chat_id, text = "Впишите значение: ")
        bot.register_next_step_handler(message, value_volume)


    elif(message.text == "look" or message.text == "заблочить"):
        bot.delete_message(my_chat_id, message.message_id)
        screen_lock()

    elif(message.text == "sec dimming" or message.text == "секунда"):
        bot.delete_message(my_chat_id, message.message_id)
        screen_dimming_every_second()
    elif(message.text == "hour dimming" or message.text == "час"):
        bot.delete_message(my_chat_id, message.message_id)
        screen_dimming_every_hour()

    elif(message.text == "ssh start" or message.text == "ссш старт"):
        bot.send_message(my_chat_id, text = ssh_start(value))
    elif(message.text == "ssh stop" or message.text == "ссш стоп"):
        bot.send_message(my_chat_id, text = ssh_stop(value))
    elif(message.text == "ssh status" or message.text == "ссш статус"):
        print(ssh_status())
        bot.send_message(my_chat_id, text = ssh_status())

    elif(message.text == "xrdp start" or message.text == "хрдп старт"):
        bot.send_message(my_chat_id, text = xrdp_start(value))
    elif(message.text == "xrdp stop" or message.text == "хрдп стоп"):
        bot.send_message(my_chat_id, text = xrdp_stop(value))
    elif(message.text == "xrdp status" or message.text == "хрдп статус"):
        bot.send_message(my_chat_id, text = xrdp_status())

def value_volume(message):
    volume_sound_expose(int(message.text))
    del_message(3, message)

from time import sleep
def del_message(num, message):
    try:
        i = 0
        num = num + 1
        while(i + 1 < num):
            bot.delete_message(message.chat.id, message.message_id - i+1)
            i += 1
    except:                 
        return

def buttons_menu():
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    music = types.KeyboardButton("музыка")
    ssh = types.KeyboardButton("ssh")
    xrdp = types.KeyboardButton("xrdp")
    screen = types.KeyboardButton("экран")
    volume = types.KeyboardButton("громкость")
    buttons.row(music, volume)
    buttons.row(screen, ssh, xrdp)
    return buttons

def buttons_volume():
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    plus = types.KeyboardButton("+")
    value = types.KeyboardButton("value")
    minus = types.KeyboardButton("-")
    back = types.KeyboardButton("назад")
    buttons.row(minus, value, plus)
    buttons.row(back)
    return buttons

def buttons_screen():
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    look = types.KeyboardButton("look")
    sec_dimming = types.KeyboardButton("sec dimming")
    hour_dimming = types.KeyboardButton("hour dimming")
    back = types.KeyboardButton("назад")
    buttons.row(look, sec_dimming, hour_dimming)
    buttons.row(back)
    return buttons

def buttons_ssh():
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("назад")
    start = types.KeyboardButton("ssh start")
    stop = types.KeyboardButton("ssh stop")
    status = types.KeyboardButton("ssh status")
    buttons.row(start, status, stop)
    buttons.row(back)
    return buttons

def buttons_xrdp():
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("назад")
    start = types.KeyboardButton("xrdp start")
    stop = types.KeyboardButton("xrdp stop")
    status = types.KeyboardButton("xrdp status")
    buttons.row(start, status, stop)
    buttons.row(back)
    return buttons

bot.polling(none_stop=True)