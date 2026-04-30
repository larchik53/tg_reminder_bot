# handlers.py - Обработчики команд бота
from config import bot
from service import parse_birthday_input, save_birthday, load_user_birthdays, nearest_birthday, parse_reminder_input, \
	save_reminder
from ui import (
	get_main_menu, get_birthday_menu, get_plans_menu,
	format_birthday_success, format_birthday_error,
	format_birthday_list, format_birthday_instructions, get_creat_menu, format_nearest_day,
	format_reminder_instructions, add_reminder, successfull_reminder_fn
)
from functions import mark_reminder_done


@bot.message_handler(commands=["start"])
def start_handler(message):
	"""Главное меню"""
	markup = get_main_menu()
	
	bot.send_message(
		message.chat.id,
		"✨ *Ваш личный помощник* ✨\n\nВыберите действие:",
		parse_mode='Markdown',
		reply_markup=markup
	)


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
	"""Обрабатывает все сообщения"""
	text = message.text
	
	# ===== ГЛАВНОЕ МЕНЮ =====
	if text == "⏰ Мои напоминания":
		show_plans_menu(message)
	
	elif text == "➕ Создать новое":
		show_creat_menu(message)
	
	elif text == "🎂 Дни рождения":
		show_birthday_menu(message)
	
	elif text == "📊 Статистика":
		bot.send_message(message.chat.id, "📊 *Статистика*\n\nВ разработке...", parse_mode='Markdown')
	
	elif text == "⬅️ Назад":
		start_handler(message)
	
	# ===== МЕНЮ ДНЕЙ РОЖДЕНИЯ =====
	elif text == "➕ Добавить День Рождение":
		ask_for_birthday(message)
	
	elif text == "📋 Список ДР":
		show_birthday_list(message)
	
	elif text == "⏰ Ближайший День Рождения":
		show_nearest_line(message)
	
	# ===== МЕНЮ ПЛАНОВ =====
	elif text == "📝 Планы на день":
		bot.send_message(message.chat.id, "📝 *Планы на день*\n\nВ разработке...", parse_mode='Markdown')
	
	elif text == "🛒 Обновить список покупок":
		bot.send_message(message.chat.id, "🛒 *Список покупок*\n\nВ разработке...", parse_mode='Markdown')
	
	elif text == "⏰ Тайм-менеджер":
		bot.send_message(message.chat.id, "⏰ *Тайм-менеджер*\n\nВ разработке...", parse_mode='Markdown')
	
	elif text == "➕ Добавить напоминание":
		ask_for_reminder(message)
	
	# ===== ОБРАБОТКА ВВОДА ДНЕЙ РОЖДЕНИЯ =====
	elif "." in text and len(text.split()) >= 2:
		process_birthday_input(message)
	
	# ===== ОБРАБОТКА ВВОДА НАПОМИНАНИЙ =====
	elif ":" in text and len(text.split()) >= 2:
		process_reminder_input(message)
	
	# ===== ОБРАБОТКА КНОПОК ВЫБОРА =====
	elif text == "✅ Сделано":
		successfull_done(message)
	
	elif text == "❌ пока не сделано":
		not_done_handler(message)
	
	# ===== ЕСЛИ НИЧЕГО НЕ ПОДОШЛО =====
	else:
		start_handler(message)


# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========
def show_birthday_menu(message):
	"""Показывает меню дней рождения"""
	markup = get_birthday_menu()
	bot.send_message(
		message.chat.id,
		"🎂 *Дни рождения*\n\nВыберите действие:",
		parse_mode='Markdown',
		reply_markup=markup
	)


def show_plans_menu(message):
	"""Показывает меню планов"""
	markup = get_plans_menu()
	bot.send_message(
		message.chat.id,
		"⏰ *Мои напоминания*\n\nВыберите раздел:",
		parse_mode='Markdown',
		reply_markup=markup
	)


def ask_for_birthday(message):
	"""Просит ввести день рождения"""
	text = format_birthday_instructions()
	bot.send_message(message.chat.id, text, parse_mode='Markdown')


def ask_for_reminder(message):
	"""Просит ввести напоминание"""
	text = format_reminder_instructions()
	bot.send_message(message.chat.id, text, parse_mode='Markdown')


def show_birthday_list(message):
	"""Показывает список дней рождения"""
	user_id = message.from_user.id
	birthdays = load_user_birthdays(user_id)
	
	text = format_birthday_list(birthdays)
	bot.send_message(message.chat.id, text, parse_mode='Markdown')


def show_nearest_line(message):
	'''Показывает ближайший день рождения'''
	user_id = message.from_user.id
	nearest_days, name_input, is_passed = nearest_birthday(user_id)
	text = format_nearest_day(nearest_days, name_input, is_passed)
	bot.send_message(message.chat.id, text, parse_mode='Markdown')


def process_birthday_input(message):
	"""Обрабатывает введенный день рождения"""
	user_id = message.from_user.id
	user_text = message.text
	
	result = parse_birthday_input(user_text)
	
	if not result["success"]:
		error_msg = format_birthday_error(result["error"])
		bot.reply_to(message, error_msg, parse_mode='Markdown')
		return
	
	save_result = save_birthday(user_id, result["date"], result["name"])
	
	if not save_result["success"]:
		error_msg = format_birthday_error(save_result["message"])
		bot.reply_to(message, error_msg, parse_mode='Markdown')
		return
	
	success_msg = format_birthday_success(result["name"], result["date"])
	bot.reply_to(message, success_msg, parse_mode='Markdown')
	
	if save_result.get("is_today"):
		bot.send_message(
			message.chat.id,
			f"🎉 И сразу же: сегодня день рождения у {save_result.get('name', result['name'])}! 🎂\n\nНе забудьте поздравить!",
			parse_mode='Markdown'
		)


def process_reminder_input(message):
	"""Обрабатывает введение напоминания"""
	user_id = message.from_user.id
	user_text = message.text
	
	result = parse_reminder_input(user_text)
	
	if not result["success"]:
		error_msg = format_birthday_error(result.get("error", "Ошибка парсинга"))
		bot.reply_to(message, error_msg, parse_mode='Markdown')
		return
	
	save_result_reminder = save_reminder(user_id, result["date"], result["name"])
	
	if not save_result_reminder["success"]:
		error_msg = format_birthday_error(save_result_reminder["message"])
		bot.reply_to(message, error_msg, parse_mode='Markdown')
		return
	
	successfull_reminder = successfull_reminder_fn(result["date"], result["name"])
	bot.reply_to(message, successfull_reminder, parse_mode='Markdown')
	
	if save_result_reminder.get("is_now"):
		bot.send_message(
			message.chat.id,
			f"⏰ И сразу же: сейчас время для '{result['name']}'!",
			parse_mode='Markdown'
		)


def show_creat_menu(message):
	"""Показывает добавочное меню"""
	markup = get_creat_menu()
	bot.send_message(
		message.chat.id,
		"🎂 *Меню создания*\n\nВыберите действие:",
		parse_mode='Markdown',
		reply_markup=markup
	)


def add_function_reminder(user_id):
	"""Отправляет меню выбора 'Сделано/Не сделано' пользователю"""
	try:
		markup = add_reminder()
		bot.send_message(
			user_id,
			"⏰ *Выполнили ли вы задачу?*\n\nОтметьте ниже:",
			parse_mode='Markdown',
			reply_markup=markup
		)
		print(f"📋 Меню выбора отправлено пользователю {user_id}")
	except Exception as e:
		print(f"❌ Ошибка отправки меню пользователю {user_id}: {e}")


def successfull_done(message):
	"""Обработка кнопки 'Сделано'"""
	try:
		user_id = message.from_user.id
		
		from config import last_reminder_for_user
		
		if user_id in last_reminder_for_user:
			reminder_text = last_reminder_for_user[user_id]
			
			if mark_reminder_done(user_id, reminder_text):
				bot.send_message(
					message.chat.id,
					f"✅ *Отлично!*\n\nЗадача '{reminder_text[:50]}...' отмечена как выполненная!",
					parse_mode='Markdown'
				)
				
				# Возвращаем главное меню
				bot.send_message(
					message.chat.id,
					"✨ Возвращаюсь в главное меню ✨",
					parse_mode='Markdown',
					reply_markup=get_main_menu()
				)
				
				# Очищаем последнее напоминание
				last_reminder_for_user.pop(user_id, None)
			else:
				bot.send_message(
					message.chat.id,
					"⚠️ Не удалось отметить задачу как выполненную",
					parse_mode='Markdown'
				)
		else:
			bot.send_message(
				message.chat.id,
				"❌ Не найдено активных напоминаний",
				parse_mode='Markdown'
			)
	
	except Exception as e:
		print(f"❌ Ошибка в successfull_done: {e}")
		bot.send_message(
			message.chat.id,
			"⚠️ Произошла ошибка при обработке",
			parse_mode='Markdown'
		)


def not_done_handler(message):
	"""Обработка кнопки 'пока не сделано'"""
	try:
		user_id = message.from_user.id
		
		from config import last_reminder_for_user
		
		# Просто очищаем последнее напоминание
		if user_id in last_reminder_for_user:
			reminder_text = last_reminder_for_user.pop(user_id, None)
			print(f"⏳ Пользователь {user_id} отложил задачу: {reminder_text[:30]}")
		
		bot.send_message(
			message.chat.id,
			"⏳ *Хорошо!*\n\nНапомню позже.",
			parse_mode='Markdown'
		)
		
		# Возвращаем в главное меню
		bot.send_message(
			message.chat.id,
			"✨ Возвращаюсь в главное меню ✨",
			parse_mode='Markdown',
			reply_markup=get_main_menu()
		)
	
	except Exception as e:
		print(f"❌ Ошибка в not_done_handler: {e}")
		bot.send_message(
			message.chat.id,
			"⚠️ Произошла ошибка",
			parse_mode='Markdown'
		)