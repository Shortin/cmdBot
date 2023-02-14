import os 
from subprocess import Popen, PIPE
from datetime import datetime

# Функция находит и возвращает название песни и имя артиста
def checkNameTrack():
    try:
        command = "playerctl -l"
        pipe = os.popen(command)
        if(pipe.read() != ""):
            check = os.popen('playerctl metadata').read().split("\n")
            name_track = check[1].split("title")
            name_track = name_track[1].strip()
            name_artist = check[3].split("artist")
            name_artist = name_artist[1].strip()
            return name_track, name_artist
        else:
            return "Плеер выключен"
    except:
        print(f'Произошла ошибка  при поиске названия песни\nВремя:{datetime.now()}')
        return False

# Останавливает илил заускает песню
def music_play_pause():
    command = "playerctl -l"
    pipe = os.popen(command)
    if(pipe.read() != ""):
        command = 'playerctl play-pause'
        os.system(command)
        return True
    else:
        return "Плеер выключен"

# Запускает следующую песню
def music_next():
    command = "playerctl -l"
    pipe = os.popen(command)
    if(pipe.read() != ""):
        command = 'playerctl next'
        os.system(command)
        return True
    else:
        return "Плеер выключен"

def status_player():
    command = "playerctl status"
    pipe = os.popen(command)
    status = pipe.read()[:-1]
    if(status == "Playing"):
        return True
    else:
        return False

# Функция прибавляет звук системы
def volume_sound_increase(value):
    try:
        checkVolume = os.popen('amixer -D pulse').read().split('[')
        checkVolume = checkVolume[1].split('%')[0]
        checkVolume = int(checkVolume) + value
        if(checkVolume >= 100):
            os.system (f'pactl set-sink-volume @DEFAULT_SINK@ 100%')
            return "100"
        os.system (f'pactl set-sink-volume @DEFAULT_SINK@ +{value}%')
        return checkVolume
    except:
        print(f'Произошла ошибка  при увеличении звука\nВремя:{datetime.now()}')
        return False

# Функция убaвляет звук системы
def volume_sound_decrease(value):
    try:
        checkVolume = os.popen('amixer -D pulse').read().split('[')
        checkVolume = checkVolume[1].split('%')[0]
        checkVolume = int(checkVolume) - value
        if(checkVolume <= 0):
            os.system (f'pactl set-sink-volume @DEFAULT_SINK@ 0%')
            return "0"
        os.system (f'pactl set-sink-volume @DEFAULT_SINK@ -{value}%')
        return checkVolume
    except:
        print(f'Произошла ошибка  при уменьшении звука\nВремя:{datetime.now()}')
        return False


# Функция выставляет выбраное знаение звука системы
def volume_sound_expose(value):
    try:
        if(value <= 0):
            os.system ('pactl set-sink-volume @DEFAULT_SINK@ 0%')
            return "0"
        elif(value >= 100):
            os.system ('pactl set-sink-volume @DEFAULT_SINK@ 100%')
            return "100"
        else:
            os.system (f'pactl set-sink-volume @DEFAULT_SINK@ {value}%')
            return value
    except:
        print(f'Произошла ошибка  при выставлениии звука\nВремя:{datetime.now()}')
        return False
        
def volume_value():
    try:
        volume = os.popen('amixer -D pulse').read().split('[')
        volume = volume[1].split('%')[0]
        return volume
    except:
        print(f'Произошла ошибка  при выведении звука\nВремя:{datetime.now()}')
        return False