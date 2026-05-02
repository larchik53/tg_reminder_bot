# ui.py - Кнопки и оформление сообщений
from telebot import types


def get_main_menu():
	"""Создает главное меню"""
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	
	btn1 = types.KeyboardButton("⏰ Мои напоминания")
	btn2 = types.KeyboardButton("➕ Создать новое")
	btn3 = types.KeyboardButton("🎂 Дни рождения")
	btn4 = types.KeyboardButton("📊 Статистика")
	
	markup.add(btn1, btn2, btn3, btn4)
	return markup


def get_birthday_menu():
	"""Создает меню дней рождения"""
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	
	btn1 = types.KeyboardButton("➕ Добавить День Рождение")
	btn2 = types.KeyboardButton("📋 Список ДР")
	btn3 = types.KeyboardButton("⏰ Ближайший День Рождения")
	btn4 = types.KeyboardButton("⬅️ Назад")
	
	markup.add(btn1, btn2, btn3, btn4)
	return markup


def get_plans_menu():
	"""Создает меню планов"""
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	
	btn1 = types.KeyboardButton("📝 Планы на день")
	btn2 = types.KeyboardButton("➕ Добавить напоминание")
	btn3 = types.KeyboardButton("🛒 Список покупок")
	btn4 = types.KeyboardButton("⬅️ Назад")
	
	markup.add(btn1, btn2, btn3, btn4)
	return markup


def get_creat_menu():
	"""Создает меню создания"""
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	
	btn1 = types.KeyboardButton("➕ Добавить День Рождение")
	btn2 = types.KeyboardButton("➕ Добавить напоминание")
	btn3 = types.KeyboardButton("🛒 Список покупок")
	btn4 = types.KeyboardButton("⬅️ Назад")
	
	markup.add(btn1, btn2, btn3, btn4)
	return markup


def format_birthday_success(name, date):
	"""Форматирует сообщение об успешном добавлении"""
	return f"✅ *Сохранено!*\n\n👤 {name}\n📅 {date}\n\nДень рождения добавлен! 🎉"


def format_birthday_error(error):
	"""Форматирует сообщение об ошибке"""
	return f"❌ *Ошибка!*\n\n{error}"


def format_birthday_list(birthdays):
	"""Форматирует список дней рождения"""
	if not birthdays:
		return "📭 *Список пуст*\n\nДобавьте первый день рождения!"
	
	text = "📋 *Ваши дни рождения:*\n\n"
	for i, bd in enumerate(birthdays, 1):
		text += f"{i}. {bd['date']} - {bd['name']}\n"
	
	text += f"\n🎂 Всего: **{len(birthdays)}** дней рождения"
	return text


def format_nearest_day(nearest_days, name_input, is_passed=False):
	"""Форматирование с учетом прошедших дней рождений"""
	if nearest_days is None or name_input is None:
		return "📭 *Дней рождений нет*\n\nДобавьте первый день рождения!"
	
	text = "🎂 *Ближайший день рождения:*\n\n"
	text += f"👤 У: **{name_input}**\n"
	
	if is_passed:
		if nearest_days > 330:
			text += f"📅 Был недавно, следующий через: **{nearest_days} дней**"
		else:
			text += f"📅 Через: **{nearest_days} дней**"
	else:
		if nearest_days == 0:
			text += "🎉 **СЕГОДНЯ!** 🎉"
		elif nearest_days == 1:
			text += "⏰ Через: **1 день** (завтра!)"
		elif nearest_days <= 7:
			text += f"🔥 Через: **{nearest_days} дней** (скоро!)"
		else:
			text += f"📅 Через: **{nearest_days} дней**"
	
	return text


def format_birthday_instructions():
	"""Инструкция по добавлению дня рождения"""
	return (
		"🎂 *Введите день рождения:*\n\n"
		"Формат: `12.10 Ваня`\n"
		"Пример: `25.12 Мама`\n\n"
		"Просто напишите дату и имя:"
	)


def format_reminder_instructions():
	"""Инструкция по добавлению напоминания"""
	return (
		"⏰ *Введите напоминание:*\n\n"
		"Формат: `время напоминание`\n"
		"Пример: `15:15 вынести мусор`\n\n"
		"Просто напишите время и текст напоминания:"
	)


def add_reminder():
	"""Создает кнопки выбора 'Сделано/Не сделано'"""
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	
	btn1 = types.KeyboardButton("❌ пока не сделано")
	btn2 = types.KeyboardButton("✅ Сделано")
	
	markup.add(btn1, btn2)
	return markup


def successfull_reminder_fn(date, name):
	"""Форматирует сообщение об успешном добавлении напоминания"""
	return f"✅ *Сохранено!*\n\n⏰ Напоминание: {name}\n📅 Время: {date}\n\nНапоминание добавлено!"

def format_reminder_list(reminders):
    """Форматирует список напоминаний"""
    if not reminders:
        return "Список напоминаний пуст."

    text = "Ваши напоминания:\n\n"

    for i, reminder in enumerate(reminders, 1):
        text += f"{i}. {reminder['time']} — {reminder['text']}\n"

    return text
def format_reminder_list(reminders):
    """Форматирует список напоминаний."""
    if not reminders:
        return "У тебя пока нет активных напоминаний."

    text = "Твои активные напоминания:\n\n"

    for i, reminder in enumerate(reminders, 1):
        text += f"{i}. {reminder['time']} — {reminder['text']}\n"

    return text