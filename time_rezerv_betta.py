# bot.py - Главный файл для запуска бота
from config import bot
from functions import start_background_worker
import handlers  # Импортируем обработчики


def main():
	# Запускаем фоновый worker
	start_background_worker()
	
	# Запускаем бота
	print("🤖 Бот запущен...")
	bot.polling(none_stop=True)


if __name__ == "__main__":
	main()



# config.py - Храним настройки и глобальные переменные
import telebot

# Токен бота
TOKEN = '8546334714:AAH5bYRtYBlTcFvfrYqUPwttWRFGh5DhID0'

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Глобальные переменные
cached_data = None
last_update = None
update_interval = 5  # 1 час в секундах
current_day = None
current_month = None
congratu_challenge = None
already_congratulated = {}

# Имя файла с днями рождения
BIRTHDAY_FILE = 'birthday_fail.txt'






import time
import threading
from datetime import datetime
from config import bot, already_congratulated, BIRTHDAY_FILE, current_day, current_month, update_interval
import config

def update_cache():
    """Твой старый код - не меняем!"""
    try:
        with open(BIRTHDAY_FILE, 'r', encoding='utf-8') as split_file:
            for line in split_file:
                # ... твой код ...
                pass
    except Exception as e:
        print(f"❌ Ошибка обновления кэша: {e}")

def send_birthday_congrats(user_id, name):
    """Твой старый код - не меняем!"""
    try:
        message_text = f"сегодня у {name.upper()} день рождения! 🎂\n\nНе забудьте поздравить!"
        bot.send_message(user_id, message_text)
        return True
    except Exception as e:
        print(f"✗ Ошибка отправки сообщения {user_id}: {e}")
        return False

def auto_update_worker():
    """Твой старый код - не меняем!"""
    while True:
        update_cache()
        today = datetime.now()
        config.current_day = today.day
        config.current_month = today.month
        time.sleep(update_interval)

def start_background_worker():
    """Твой старый код - не меняем!"""
    thread = threading.Thread(target=auto_update_worker, daemon=True)
    thread.start()
    print("✅ Фоновый worker запущен")

def show_plans_menu(message):
	pass



def show_create_menu(message):
	pass



def show_birthday_list(message):
	pass


def show_statistics(message):
	pass

def creat_new_reminder(message):
	pass


from datetime import datetime

BIRTHDAY_FILE = 'birthday_fail.txt'


# 1. Функция парсинга ввода
def parse_birthday_text(text):
	"""
	Разбирает "12.10 Ваня" на части
	Возвращает: {"success": True/False, "date": "...", "name": "...", "error": "..."}
	"""
	user_input = text.strip()
	user_input = ' '.join(user_input.split())
	parts = user_input.split(maxsplit=1)
	
	if len(parts) != 2:
		return {
			"success": False,
			"error": "❌ Неверный формат!\nВведи: дата имя\nПример: 12.12.2024 Мама"
		}
	
	date_str, name = parts
	return {
		"success": True,
		"date": date_str,
		"name": name
	}


# 2. Функция сохранения (твой код, только возвращает результат)
def save_birthday(user_id, date_str, name):
	"""Сохраняет день рождения в файл"""
	try:
		birth_line = f'{user_id} {date_str} {name}\n'
		with open(BIRTHDAY_FILE, 'a', encoding='utf-8') as file:
			file.write(birth_line)
		
		return {"success": True, "message": "Сохранено успешно!"}
	except Exception as e:
		return {"success": False, "message": f"Ошибка: {str(e)}"}


# 3. Функция загрузки дней рождения
def load_user_birthdays(user_id):
	"""Загружает дни рождения пользователя"""
	birthdays = []
	
	try:
		with open(BIRTHDAY_FILE, 'r', encoding='utf-8') as file:
			for line in file:
				line = line.strip()
				if not line:
					continue
				
				parts = line.split(maxsplit=2)
				if len(parts) == 3 and parts[0] == str(user_id):
					birthdays.append({
						"date": parts[1],
						"name": parts[2]
					})
	except FileNotFoundError:
		pass
	
	return birthdays


from config import bot
from service import parse_birthday_text, save_birthday, load_user_birthdays
from ui import (
	get_main_menu, get_birthday_menu, get_plans_menu,
	format_birthday_success, format_birthday_error,
	format_birthday_list, format_birthday_instructions
)


@bot.message_handler(commands=["start"])
def start_handler(message):
	markup = get_main_menu()
	bot.send_message(
		message.chat.id,
		"✨ Ваш личный помощник ✨\n\nВыберите действие:",
		parse_mode='Markdown',
		reply_markup=markup
	)


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
	text = message.text
	
	# Главное меню
	if text == "📅 Планы на день":
		show_plans_menu(message)
	
	elif text == "➕ Создать новое":
		bot.send_message(message.chat.id, "➕ Создание нового")
	
	elif text == "🎂 Дни рождения":
		show_birthday_menu(message)
	
	elif text == "📊 Статистика":
		bot.send_message(message.chat.id, "📊 Статистика")
	
	elif text == "⬅️ Назад":
		start_handler(message)
	
	# Меню дней рождения
	elif text == "➕ Добавить ДР":
		ask_for_birthday(message)
	
	elif text == "📋 Список ДР":
		show_birthday_list(message)
	
	elif text == "⏰ Ближайший ДР":
		bot.send_message(message.chat.id, "⏰ Ближайший ДР")
	
	# Меню планов
	elif text == "📝 Список дел":
		bot.send_message(message.chat.id, "📝 Список дел")
	
	elif text == "🛒 Список покупок":
		bot.send_message(message.chat.id, "🛒 Список покупок")
	
	elif text == "⏰ Тайм-менеджер":
		bot.send_message(message.chat.id, "⏰ Тайм-менеджер")
	
	# Обработка ввода дня рождения
	elif "." in text and len(text.split()) >= 2:
		process_birthday_input(message)


# Вспомогательные функции (только вызовы!)
def show_birthday_menu(message):
	markup = get_birthday_menu()
	bot.send_message(
		message.chat.id,
		"🎂 Дни рождения",
		parse_mode='Markdown',
		reply_markup=markup
	)


def show_plans_menu(message):
	markup = get_plans_menu()
	bot.send_message(
		message.chat.id,
		"📅 Планы на день",
		parse_mode='Markdown',
		reply_markup=markup
	)


def ask_for_birthday(message):
	text = format_birthday_instructions()
	bot.send_message(message.chat.id, text, parse_mode='Markdown')


def show_birthday_list(message):
	user_id = message.from_user.id
	birthdays = load_user_birthdays(user_id)
	
	text = format_birthday_list(birthdays)
	bot.send_message(message.chat.id, text, parse_mode='Markdown')


def process_birthday_input(message):
	"""Заменил handle_all_text - теперь только вызывает функции"""
	user_id = message.from_user.id
	user_text = message.text
	
	# 1. Парсим текст (services.py)
	result = parse_birthday_text(user_text)
	
	# 2. Если ошибка - показываем (ui.py)
	if not result["success"]:
		error_msg = format_birthday_error(result["error"])
		bot.reply_to(message, error_msg)
		return
	
	# 3. Сохраняем (services.py)
	save_result = save_birthday(user_id, result["date"], result["name"])
	
	# 4. Если ошибка сохранения
	if not save_result["success"]:
		error_msg = format_birthday_error(save_result["message"])
		bot.reply_to(message, error_msg)
		return
	
	# 5. Всё ок! Показываем успех (ui.py)
	success_msg = format_birthday_success(result["name"], result["date"])
	bot.reply_to(message, success_msg)


# ui.py - красивые сообщения и кнопки
from telebot import types


# 1. Кнопки (твои старые функции, просто выносим их сюда)
def get_main_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn1 = types.KeyboardButton("📅 Планы на день")
	btn2 = types.KeyboardButton("➕ Создать новое")
	btn3 = types.KeyboardButton("🎂 Дни рождения")
	btn4 = types.KeyboardButton("📊 Статистика")
	markup.add(btn1, btn2, btn3, btn4)
	return markup


def get_birthday_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn1 = types.KeyboardButton("➕ Добавить ДР")
	btn2 = types.KeyboardButton("📋 Список ДР")
	btn3 = types.KeyboardButton("⏰ Ближайший ДР")
	btn4 = types.KeyboardButton("⬅️ Назад")
	markup.add(btn1, btn2, btn3, btn4)
	return markup


def get_plans_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn1 = types.KeyboardButton("📝 Список дел")
	btn2 = types.KeyboardButton("🛒 Список покупок")
	btn3 = types.KeyboardButton("⏰ Тайм-менеджер")
	btn4 = types.KeyboardButton("⬅️ Назад")
	markup.add(btn1, btn2, btn3, btn4)
	return markup


# 2. Форматирование сообщений (твои старые тексты)
def format_birthday_success(name, date):
	return f"✅ Сохранено!\nДля {name} на дату {date}"


def format_birthday_error(error):
	return f"❌ Ошибка!\n{error}"


def format_birthday_list(birthdays):
	if not birthdays:
		return "📭 Список пуст\n\nДобавьте первый день рождения!"
	
	text = "📋 Ваши дни рождения:\n\n"
	for i, bd in enumerate(birthdays, 1):
		text += f"{i}. {bd['date']} - {bd['name']}\n"
	
	text += f"\nВсего: {len(birthdays)}"
	return text


def format_birthday_instructions():
	return "🎂 Введите день рождения:\n\nФормат: 12.10 Ваня\nПример: 25.12 Мама"