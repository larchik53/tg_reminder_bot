# services.py - Логика обработки данных
from config import BIRTHDAY_FILE, REMINDER_FILE
from datetime import datetime, date
from config import REMINDER_FILE


def parse_birthday_input(text):
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
			"error": "❌ Неверный формат!\nВведи: дата имя\nПример: 12.12 Мама"
		}
	
	date_str, name = parts
	
	# Простая проверка даты
	if not is_valid_date(date_str):
		return {
			"success": False,
			"error": f"❌ Неверная дата: {date_str}\nИспользуйте формат: ДД.ММ"
		}
	
	return {
		"success": True,
		"date": date_str,
		"name": name
	}


def parse_reminder_input(text):
	"""Разбирает "15:15 вынести мусор" на части"""
	user_input = text.strip()
	user_input = ' '.join(user_input.split())
	parts_reminder = user_input.split(maxsplit=1)
	
	# Проверяем что есть 2 части (время и текст)
	if len(parts_reminder) != 2:
		return {
			"success": False,
			"error": "❌ Неверный формат!\nВведи: время напоминание\nПример: 15:15 вынести мусор"
		}
	
	time_str, reminder = parts_reminder
	
	# Проверяем валидность времени
	if not is_valid_reminder(time_str):
		return {
			"success": False,
			"error": f"❌ Неверное время: {time_str}\nИспользуйте формат: часы:минуты (например 15:30)"
		}
	
	return {
		"success": True,
		"date": time_str,
		"name": reminder
	}


def is_valid_reminder(time_str):
	"""Проверяет валидность времени"""
	try:
		if ':' not in time_str:
			return False
		
		parts = time_str.split(':')
		
		if len(parts) != 2:
			return False
		
		hour = int(parts[0])
		minute = int(parts[1])
		
		return 0 <= hour <= 23 and 0 <= minute <= 59
	
	except (ValueError, IndexError):
		return False


def is_valid_date(date_str):
	"""Проверяет, похоже ли на дату"""
	try:
		if '.' not in date_str:
			return False
		
		parts = date_str.split('.')
		if len(parts) < 2:
			return False
		
		day = int(parts[0])
		month = int(parts[1])
		
		return 1 <= day <= 31 and 1 <= month <= 12
	except:
		return False


def save_birthday(user_id, date_str, name):
	"""Сохраняет день рождения в файл"""
	try:
		birth_line = f'{user_id} {date_str} {name}\n'
		with open(BIRTHDAY_FILE, 'a', encoding='utf-8') as file:
			file.write(birth_line)
		
		# Проверяем не сегодняшний ли это ДР
		today = datetime.now()
		
		try:
			clean_date = date_str.replace(',', '.')
			parts = clean_date.split('.')
			
			if len(parts) >= 2:
				day = int(parts[0])
				month = int(parts[1])
				
				if day == today.day and month == today.month:
					print(f"⚡ [SERVICES] Сегодня день рождения у {name}!")
					
					return {
						"success": True,
						"message": "День рождения сохранен! (и сегодня ДР!)",
						"is_today": True,
						"name": name
					}
		except:
			pass
		
		return {
			"success": True,
			"message": "День рождения сохранен!",
			"is_today": False
		}
	except Exception as e:
		return {"success": False, "message": f"Ошибка: {str(e)}"}


def save_reminder(user_id, time_str, reminder):
	"""Сохраняет напоминание в файл"""
	try:
		reminder_line = f'{user_id} {time_str} {reminder}\n'
		with open(REMINDER_FILE, 'a', encoding='utf-8') as file:
			file.write(reminder_line)
		
		# Проверяем не сейчас ли это напоминание
		now = datetime.now()
		current_hour = now.hour
		current_minute = now.minute
		
		try:
			time_str_strip = time_str.strip()
			parts = time_str_strip.split(':')
			
			if len(parts) == 2:
				hour = int(parts[0])
				minute = int(parts[1])
				
				if hour == current_hour and minute == current_minute:
					return {
						"success": True,
						"message": "Напоминание сохранено! (и время пришло)",
						"is_now": True,
						"reminder": reminder
					}
		except:
			pass
		
		return {
			"success": True,
			"message": "Напоминание сохранено!",
			"is_now": False
		}
	except Exception as e:
		return {"success": False, "message": f"Ошибка: {str(e)}"}


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


def nearest_birthday(user_id):
	"""Функция для поиска ближайшего дня рождения с учетом прошедших дат"""
	nearest_day = None
	nearest_name = None
	is_passed = False
	
	try:
		with open(BIRTHDAY_FILE, 'r', encoding='utf-8') as file:
			lines = file.readlines()
			
			if not lines:
				return None, None, None
			
			today = datetime.now().date()
			current_year = today.year
			
			for line in lines:
				line = line.strip()
				if not line:
					continue
				
				try:
					list_by_parts = line.split(maxsplit=2)
					if len(list_by_parts) < 3:
						continue
					file_user_id = int(list_by_parts[0])
					if file_user_id != user_id:
						continue
					data_input = list_by_parts[1]
					name_input = list_by_parts[2]
					
					clean_date = data_input.replace(',', '.')
					parts = clean_date.split('.')
					if len(parts) < 2:
						continue
					
					day = int(parts[0])
					month = int(parts[1])
					
					try:
						event_date_current = date(current_year, month, day)
					except ValueError:
						continue
					
					days_diff_current = (event_date_current - today).days
					passed_this_year = days_diff_current < 0
					
					if passed_this_year:
						try:
							event_date_next = date(current_year + 1, month, day)
						except ValueError:
							next_year = current_year + 1
							while not (next_year % 4 == 0 and (next_year % 100 != 0 or next_year % 400 == 0)):
								next_year += 1
							event_date_next = date(next_year, month, day)
						
						days_left = (event_date_next - today).days
						is_passed_for_this = True
					else:
						days_left = days_diff_current
						is_passed_for_this = False
					
					if nearest_day is None or days_left < nearest_day:
						nearest_day = days_left
						nearest_name = name_input
						is_passed = is_passed_for_this
				
				except (ValueError, IndexError):
					continue
		
		return nearest_day, nearest_name, is_passed
	
	except FileNotFoundError:
		return None, None, None
	
def remove_user_reminder(user_id, reminder_text):
    """Удаляет выполненное напоминание из файла."""
    from config import REMINDER_FILE

    lines = []

    try:
        with open(REMINDER_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if reminder_text not in line or str(user_id) not in line:
                    lines.append(line)

        with open(REMINDER_FILE, "w", encoding="utf-8") as file:
            file.writelines(lines)

    except Exception as e:
        print(f"Ошибка удаления напоминания: {e}")



def load_user_reminders(user_id):
    """Загружает все активные напоминания пользователя."""
    reminders = []

    try:
        with open(REMINDER_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                parts = line.split(maxsplit=2)

                if len(parts) == 3 and parts[0] == str(user_id):
                    reminders.append({
                        "time": parts[1],
                        "text": parts[2]
                    })

    except FileNotFoundError:
        pass

    return reminders
