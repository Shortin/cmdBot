import os 
from subprocess import Popen, PIPE
import logging

# Функция checkNameTrack() ищет название песни и имя артиста
# функция music_play_pause() останавливает или запускает музыку
# функция next_track() включает следующий трек
# Функция status_player() проверяет остановлен или запущен плеер
# Функция status_availability_player() провряет есть ли рабочий плеер
# Функция volume_value() возвращает значение громкости плеера
# функция volume_sound_setting() устанавливает громкость  звука




# Функция checkNameTrack() ищет название песни и имя артиста
# функция возвращает название песни и имя артиста, или сообщает о том что плеер отсутсвует, при ошибке возвращает False
def checkNameTrack():
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
        return "Плеер отсутсвует"


# функция music_play_pause() останавливает или запускает музыку
# Функция возрвразает True  если все удачно, либо сообщает о том что плеер отсутсвует
def music_play_pause():
    command = "playerctl -l"
    pipe = os.popen(command)
    if(pipe.read() != ""):
        command = 'playerctl play-pause'
        os.system(command)
        return True
    else:
        return "Плеер отсутствует"

# функция next_track() включает следующий трек
# Функция next_track() возрвразает True если все удачно, или сообщает о том что плеер отсутсвует
def next_track():
    command = "playerctl -l"
    pipe = os.popen(command)
    if(pipe.read() != ""):
        command = 'playerctl next'
        os.system(command)
        return True
    else:
        return "Плеер отсутсвутет"

# Функция status_player() проверяет остановлен или запущен плеер
# Функция status_player() возрвразает True если плеер запущен или возвращает False если плеер остановлен
def status_player():
    command = "playerctl status"
    pipe = os.popen(command)
    status = pipe.read()[:-1]
    if(status == "Playing"):
        return True
    else:
        return False

# Функция status_availability_player() провряет есть ли рабочий плеер
# Функция status_availability_player() возрвразает True если плеер отсутсвует или возвращает False если плеер присутсвует
def status_availability_player():
    command = "playerctl status"
    pipe = os.popen(command)
    status = pipe.read()
    if(status == ""):
        return True
    else:
        return False

# Функция volume_value() возвращает значение громкости плеера
def volume_value():
    volume = os.popen('amixer -D pulse').read().split('[')
    volume = volume[1].split('%')[0]
    return volume

# функция volume_sound_setting() устанавливает громкость  звука
# Функция volume_sound_setting() принимает на вход значение "+число", "-число" или "число", при этом возращает значение которое получилось, если пришло неправельное значение возвращает false
def volume_sound_setting(value):
    checkVolume = volume_value()
    if(value[0] == '-'):
        checkVolume = int(checkVolume) - int(value[1:])
    elif(value[0] == '+'):
        checkVolume = int(checkVolume) + int(value[1:])
    else:
        checkVolume = int(value)
    try:        
        if(checkVolume >= 100):
                os.system (f'pactl set-sink-volume @DEFAULT_SINK@ 100%')
                return "100"
        elif(checkVolume <= 0):
                os.system (f'pactl set-sink-volume @DEFAULT_SINK@ 0%')
                return "0"
        else:
            os.system (f'pactl set-sink-volume @DEFAULT_SINK@ {checkVolume}%')
            return checkVolume
    except:
        logging.basicConfig(level=logging.error, filename="py_log.log",filemode="a", format="%(asctime)s %(levelname)s %(message)s")
        logging.error(f"функция volume_sound_setting()(soundSetting.py) выдала ошибку, на вход пришло {value}")
        return False