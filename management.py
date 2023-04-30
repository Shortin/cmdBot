import os
from subprocess import Popen, PIPE
import logging #https://habr.com/ru/companies/wunderfund/articles/683880/

# Скрипт function.py полностью переписать и немного переделан


# Функция ksksks() прдназанчена для того чтобы обратить на себя внимание Лии

# Функция screen_lock() переводит экран в режим ожидания
# Функция screen_dimming_every() ставить задержку гашения экрана равной 1 или 3600 секунды

# Функция get_external_ip() возвращает внешний ip

# Функция server_start() запускает ssh или xrdp
# Функция останавливает ssh или xrdp
# Функция выводит статус ssh или xrdp

# Функция DEAD() выключает компьютер



# Функция ksksks() считтывает показатель звука на данный момент, потом его увеличивает,после чего выводит инфомацию для привлечения внимания и убавляет звук обратно
def ksksks():
    checkVolume = os.popen('amixer -D pulse').read().split('[')
    checkVolume = checkVolume[1].split('%')[0]
    os.system('pactl set-sink-volume @DEFAULT_SINK@ 150%')
    os.system('open /home/program/newCmdBot/extras/photo1.png')
    os.system('mpg123 /home/program/newCmdBot/extras/mus1.mp3')
    os.system('mpg123 /home/program/newCmdBot/extras/mus2.mp3')
    os.system(f'pactl set-sink-volume @DEFAULT_SINK@ {checkVolume}%')
    logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="a", format="%(asctime)s %(levelname)s %(message)s")
    logging.info(f"Лия опять не отвечает?) (не ну это стеб)")


# Функция screen_lock() переводит экран в режим ожидания, делает она это благодаря встроеной в убунту команде
def screen_lock():
    try:
        os.system ('gnome-screensaver-command --lock')
        return True
    except:
        logging.basicConfig(level=logging.error, filename="py_log.log",filemode="a", format="%(asctime)s %(levelname)s %(message)s")
        logging.error("функция screen_lock()(management.py) выдала ошибку")
        return False    

# Функция screen_dimming_every() ставить задержку гашения экрана # Функция ставить задержку гашения экрана равной 1 или 3600 секунды
# функция принимает на вход строку "1" или "3600"
def screen_dimming_every(time):
	try:
		os.system (f'gsettings set org.gnome.desktop.session idle-delay {time}')
		return True
	except:
		logging.error(f'Произошла ошибка  при вызове функции screen_dimming_every()(management.py), значение переменной time: {time}')
		return False


# Функция get_external_ip() возвращает внешний ip
def get_external_ip():
	import stun
	return stun.get_ip_info()[1]


# Функция server_start() запускает ssh или xrdp, функция принимает строку "ssh" или "xrdp"
def server_start(value, checkTupe):
	try:
		command = f'sudo systemctl start {checkTupe}'.split()
		p = Popen(['sudo', '--stdin'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
		sudo_prompt = p.communicate(value + '\n')[1]
		return f"{checkTupe}-server запущен"
	except:
		logging.error(f"функция server_start()(management.py) выдала ошибку")
		return False

# Функция останавливает ssh или xrdp, функция принимает строку "ssh" или "xrdp"
def server_stop(value, checkTupe):
	try:
		command = f'sudo systemctl stop {checkTupe}'.split()
		p = Popen(['sudo', '--stdin'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
		sudo_prompt = p.communicate(value + '\n')[1]
		return f"{checkTupe}-server остановлен"
	except:
		logging.error(f"функция server_stop()(management.py) выдала ошибку")
		return False

# Функция выводит статус ssh или xrdp, функция принимает строку "ssh" или "xrdp"
def server_status(checkTupe):
	status = os.popen(f'systemctl status {checkTupe}').read().split("\n")
	return status[2].strip()

# Функция DEAD() выключает компьютер
def DEAD(value):
    logging.info(f"кмпьютор экстрнно выключен")
    command = 'sudo shutdown -h now'.split()
    p = Popen(['sudo', '--stdin'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
    sudo_prompt = p.communicate(value + '\n')[1]