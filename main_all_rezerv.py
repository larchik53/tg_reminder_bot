import telebot
import time
import threading
from datetime import datetime

cached_data = None
last_update = None
update_interval = 5  # 1 час в секундах
current_day = None
current_month = None
congratu_challenge = None
tg_token = telebot.TeleBot('8546334714:AAH5bYRtYBlTcFvfrYqUPwttWRFGh5DhID0')

already_congratulated = {}


def auto_update_worker():
	"""Фоновая задача для автообновления"""
	global current_day, current_month, update_interval  # Добавляем эту строку!
	while True:  # Бесконечный цикл
		update_cache()  # Обновляем кэш
		today = datetime.now()
		current_day = today.day
		current_month = today.month
		time.sleep(update_interval)


def start_background_worker():
	thread = threading.Thread(target=auto_update_worker, daemon=True)
	thread.start()
	print("✅ Фоновый worker запущен")


@tg_token.message_handler(commands=["start"])
def start(chat):
	tg_token.send_message(chat.chat.id, 'привет мир')


@tg_token.message_handler(commands=['plan_on_day'])
def plan_on_day(chat):
	tg_token.send_message(chat.chat.id, 'в разработке номер 4')


@tg_token.message_handler(commands=["creat_new"])
def creat(chat):
	tg_token.send_message(chat.chat.id, 'я помогу тебе запомнить важные дела')
	tg_token.send_message(chat.chat.id, 'отправь мне дату и что нужно сделать.')
	tg_token.send_message(chat.chat.id, 'В формате')


@tg_token.message_handler(commands=["active"])
def active(chat):
	tg_token.send_message(chat.chat.id, 'в разработке номер 2 ')


@tg_token.message_handler(commands=["birthday", "bithdey_day"])
def birthday_start(chat):
	# Отправляем красивое сообщение с emoji и форматированием
	tg_token.send_message(
		chat.chat.id,
		"🎂 *Дни рождения* 🎂\n\n"
		"Я запомню день рождения каждого!\n\n"
		"📝 *Как добавить:*\n"
		"Напиши в формате:\n"
		"`12.10 Ваня`\n\n"
		"📋 *Команды:*\n"
		"• /birthday - эта справка\n"
		"• /list - список всех дней рождений\n"
		"• /next - ближайший день рождения\n"
	
	)


@tg_token.message_handler(content_types=['text'])
def handle_all_text(message):
	user_input = message.text.strip()  # Сохраняем текст в переменную
	user_id = message.from_user.id
	user_input = ' '.join(user_input.split())
	parts = user_input.split(maxsplit=1)
	if len(parts) != 2:
		tg_token.reply_to(message,
		                  "❌ Неверный формат!\n"
		                  "Введи: дата имя\n"
		                  "Пример: 12.12.2024 Мама")
		return
	elif len(parts) == 3:
		user_id = parts[0]
		date_str = parts[1]
		name = parts[2]
	
	data, full_name = parts
	birth_line = f'{user_id} {data} {full_name} \n'
	with open('birthday_fail.txt', 'a', encoding='utf-8') as file:
		file.write(birth_line)


def update_cache():
	"""Обновление кэша данных из файла"""
	global cached_data, last_update, current_day, current_month, already_congratulated
	
	try:
		with open("birthday_fail.txt", 'r', encoding='utf-8') as split_file:
			for line in split_file:
				# 1. Очищаем строку
				line = line.strip()
				
				# 2. Проверяем, что строка не пустая
				if not line:
					continue
				
				# 3. Разбиваем на 3 части
				parts = line.split(maxsplit=2)
				
				# 4. Проверяем, что получилось 3 части
				if len(parts) != 3:
					print(f"⚠️  Пропущена строка (не 3 части): {line}")
					continue
				
				# 5. Извлекаем данные
				user_id = parts[0]
				date_str = parts[1]  # Используем date_str, а не line_list_data!
				full_name = parts[2]
				
				# 6. Проверяем, не поздравляли ли уже
				if user_id in already_congratulated:
					continue
				
				# 7. Обрабатываем дату
				try:
					# Заменяем запятые на точки
					date_str_clean = date_str.replace(',', '.')
					
					# Разбиваем по точке
					numbers = date_str_clean.split('.')
					
					# Проверяем, что есть хотя бы день и месяц
					if len(numbers) >= 2:
						day_num = int(numbers[0])
						month_num = int(numbers[1])
						
						# 8. Сравниваем с текущей датой
						if current_day == day_num and current_month == month_num:
							if send_birthday_congrats(int(user_id), full_name):
								already_congratulated[user_id] = True
				
				
				except ValueError as e:
					print(f"⚠️  Ошибка в дате '{date_str}': {e}")
					continue
				except Exception as e:
					print(f"⚠️  Ошибка обработки строки '{line}': {e}")
					continue
		
		last_update = datetime.now()
		print(f"🕒 Кэш обновлен: {last_update.strftime('%H:%M:%S')}")
	
	except FileNotFoundError:
		print("📭 Файл birthday_fail.txt не найден")
	except Exception as e:
		print(f"❌ Ошибка обновления кэша: {e}")


def send_birthday_congrats(user_id, name):
	"""Отправляет поздравление с днем рождения"""
	try:
		message_text = f"сегодня у {name.upper()} день рождения! 🎂\n\nНе забудьте поздравить!"
		tg_token.send_message(
			user_id,
			message_text  # ← Только один текстовый аргумент!
		)
	except telebot.apihelper.ApiTelegramException as e:
		if "Forbidden" in str(e):
			print(f"✗ Пользователь {user_id} заблокировал бота")
		else:
			print(f"✗ Ошибка Telegram API для {user_id}: {e}")
	
	except Exception as e:
		print(f"✗ Неизвестная ошибка для {user_id}: {e}")
	
	return False


start_background_worker()
tg_token.polling(none_stop=True)