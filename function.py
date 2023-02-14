import os 
from subprocess import Popen, PIPE
from datetime import datetime


# Надо прописать return в звуке, чтобы знать какое сейчас значение или то что плеер отсутсвует
# Если плеер отсутсвует надо как то открыть браузер и обновить страницу
# написать функцию которая будт открывать видео в ютюбе чтобы ставить на фон


# Функция переводит экран в режим ожидания
# def screen_lock()

# Функция ставить задержку гашения экрана равной 1 секунде
# def screen_dimming_every_second()

# Функция ставить задержку гашения экрана равной 1 часу
# def screen_dimming_every_hour()


# Функция возвращает внешний ip
# def get_external_ip()


# Функция запускает ssh
# def ssh_start(value)

# Функция останавливает ssh
# def ssh_stop(value)

# Функция выводит статус ssh
# def ssh_status()


# Функция запускает xrdp
# def xrdp_start(value)

# Функция останавливает xrdp
# def xrdp_stop(value):

# Функция выводит статус xrdp
# def xrdp_status()



# Функция переводит экран в режим ожидания
def screen_lock():
	try:
		os.system ('gnome-screensaver-command --lock')
		return True
	except:
		print(f'Произошла ошибка  при блокировке экрана\nВремя:{datetime.now()}')
		return False

# Функция ставить задержгу гашения экрана равной 1 секунде
def screen_dimming_every_second():
	try:
		os.system ('gsettings set org.gnome.desktop.session idle-delay 1')
		return True
	except:
		print(f'Произошла ошибка  при вызове функции screen_dimming_every_second()\nВремя:{datetime.now()}')
		return False

# Функция ставить задержгу гашения экрана равной 1 часу
def screen_dimming_every_hour():
	try:
		os.system ('gsettings set org.gnome.desktop.session idle-delay 3600')
		return True
	except:
		print(f'Произошла ошибка  при вызове функции screen_dimming_every_hour()\nВремя:{datetime.now()}')
		return False



# Функция возвращает внешний ip
def get_external_ip():
	import stun
	return stun.get_ip_info()[1]


# Функция запускает ssh
def ssh_start(value):
	try:
		command = 'sudo systemctl start ssh'.split()
		p = Popen(['sudo', '--stdin'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
		sudo_prompt = p.communicate(value + '\n')[1]
		return "ssh-server запущен"
	except:
		print(f'Произошла ошибка  запуске ssh\nВремя:{datetime.now()}')
		return False

# Функция останавливает ssh
def ssh_stop(value):
	try:
		command = 'sudo systemctl stop ssh'.split()
		p = Popen(['sudo', '--stdin'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
		sudo_prompt = p.communicate(value + '\n')[1]
		return "ssh-server остановлен"
	except:
		print(f'Произошла ошибка при остановке ssh\nВремя:{datetime.now()}')
		return False

# Функция выводит статус ssh
def ssh_status():
	# status = os.popen('systemctl status ssh').read().split("\n")
	# status = status[2].strip()
	return "функция временно не работает"


# Функция запускает xrdp
def xrdp_start(value):
	try:
		command = 'sudo systemctl start xrdp'.split()
		p = Popen(['sudo', '--stdin'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
		sudo_prompt = p.communicate(value + '\n')[1]
		return "xrdp-server запущен"
	except:
		print(f'Произошла ошибка при запуске xrdp\nВремя:{datetime.now()}')
		return False

# Функция останавливает xrdp
def xrdp_stop(value):
	try:
		command = 'sudo systemctl stop xrdp'.split()
		p = Popen(['sudo', '--stdin'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
		sudo_prompt = p.communicate(value + '\n')[1]
		return "xrdp-server остановлен"
	except:
		print(f'Произошла ошибка при остановке xrdp\nВремя:{datetime.now()}')
		return False

# Функция выводит статус xrdp
def xrdp_status():
	status = os.popen('systemctl status xrdp').read().split("\n")
	return status[2].strip()


# Функция выключает компьютер
def DEAD(value):
	command = 'sudo shutdown -h now'.split()
	p = Popen(['sudo', '--stdin'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
	sudo_prompt = p.communicate(value + '\n')[1]
