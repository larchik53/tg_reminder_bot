import time
import threading
from datetime import datetime
from config import BIRTHDAY_FILE, message_queue, REMINDER_FILE, message_queue_reminder
import config

print(f"🔧 [FUNCTIONS] Импортирован. BIRTHDAY_FILE = {BIRTHDAY_FILE}")


def send_reminder_message(user_id, reminder_input):
	"""Добавляет напоминание в очередь"""
	try:
		message_text = f"⏰ *Напоминание:*\n\n'{reminder_input}'"
		
		try:
			user_id_int = int(user_id)
		except ValueError:
			print(f"❌ Неверный user_id: {user_id}")
			return False
		
		# Кладем в очередь
		message_queue_reminder.put({
			'user_id': user_id_int,
			'text': message_text,
			'type': 'reminder',
			'reminder_input': reminder_input,
			'time': datetime.now().strftime("%H:%M:%S")
		})
		
		print(f"📨 Напоминание для {user_id} добавлено в очередь: {reminder_input}")
		return True
	
	except Exception as e:
		print(f"✗ Ошибка в send_reminder_message: {e}")
		import traceback
		traceback.print_exc()
		return False


def send_birthday_congrats(user_id, name):
	"""Добавляет поздравление в очередь"""
	try:
		print(f"🎂 [send_birthday_congrats] Вызвана для {user_id}, {name}")
		
		message_text = f"🎉 *Сегодня день рождения у {name.upper()}!* 🎂\n\nНе забудьте поздравить!"
		
		try:
			user_id_int = int(user_id)
		except ValueError:
			print(f"❌ Неверный user_id: {user_id}")
			return False
		
		message_queue.put({
			'user_id': user_id_int,
			'text': message_text,
			'type': 'birthday',
			'time': datetime.now().strftime("%H:%M:%S")
		})
		
		print(f"📨 Сообщение для {user_id} добавлено в очередь")
		return True
	
	except Exception as e:
		print(f"✗ Ошибка в send_birthday_congrats: {e}")
		import traceback
		traceback.print_exc()
		return False


def mark_reminder_done(user_id, reminder_text):
	"""Отмечает напоминание как выполненное"""
	try:
		user_id_str = str(user_id)
		current_date = datetime.now().strftime("%Y-%m-%d")
		
		# Добавляем в выполненные
		if user_id_str not in config.completed_reminders:
			config.completed_reminders[user_id_str] = []
		
		config.completed_reminders[user_id_str].append({
			'reminder': reminder_text,
			'completed_at': datetime.now().strftime("%H:%M:%S"),
			'date': current_date
		})
		
		print(f"✅ Напоминание отмечено как выполненное: {user_id} - {reminder_text[:30]}")
		return True
	
	except Exception as e:
		print(f"❌ Ошибка в mark_reminder_done: {e}")
		return False


def is_reminder_completed(user_id, reminder_text):
	"""Проверяет, выполнено ли напоминание сегодня"""
	try:
		user_id_str = str(user_id)
		current_date = datetime.now().strftime("%Y-%m-%d")
		
		if user_id_str not in config.completed_reminders:
			return False
		
		# Ищем среди выполненных сегодня
		for completed in config.completed_reminders[user_id_str]:
			if completed['date'] == current_date and completed['reminder'] == reminder_text:
				return True
		
		return False
	
	except Exception as e:
		print(f"❌ Ошибка в is_reminder_completed: {e}")
		return False


def update_reminder():
	'''Обрабатываем напоминания'''
	try:
		now = datetime.now()
		current_hour = now.hour
		current_minute = now.minute
		current_date = now.strftime("%Y-%m-%d")
		print(f'⏰ Сейчас {current_hour:02d}:{current_minute:02d} ({current_date})')
		
		# Проверяем существование файла
		try:
			with open(REMINDER_FILE, 'r', encoding='utf-8') as test_reminder_file:
				lines = test_reminder_file.readlines()
				print(f"📁 Файл напоминаний найден. Строк: {len(lines)}")
		except FileNotFoundError:
			print(f"📭 Файл {REMINDER_FILE} не найден!")
			return
		
		# Обрабатываем файл
		try:
			with open(REMINDER_FILE, 'r', encoding='utf-8') as file:
				for line_num, line in enumerate(file, 1):
					try:
						line = line.strip()
						if not line:
							continue
						
						parts = line.split(maxsplit=2)
						if len(parts) != 3:
							continue
						
						user_id, time_of_reminder, reminder_input = parts
						
						# Пропускаем если уже выполнили сегодня
						if is_reminder_completed(user_id, reminder_input):
							print(f"   ✅ Уже выполнено: {reminder_input[:30]}")
							continue
						
						# Проверяем уже отправляли ли сегодня
						reminder_key = f"{user_id}_{time_of_reminder}_{reminder_input}_{current_date}"
						if reminder_key in config.sent_reminders_today:
							print(f"   ⏸️ Уже отправляли сегодня: {reminder_input[:30]}")
							continue
						
						try:
							time_parts = time_of_reminder.split(':')
							if len(time_parts) < 2:
								continue
							
							hour_int = int(time_parts[0])
							minute_num = int(time_parts[1])
							
							if not (0 <= hour_int <= 23 and 0 <= minute_num <= 59):
								continue
							
							# Проверяем точное совпадение времени
							if hour_int == current_hour and minute_num == current_minute:
								print(f"   🎯 Время! Напоминание для {user_id}: {reminder_input}")
								
								# Отправляем напоминание
								if send_reminder_message(user_id, reminder_input):
									# Отмечаем как отправленное сегодня
									config.sent_reminders_today[reminder_key] = {
										'sent_at': datetime.now().strftime("%H:%M:%S"),
										'reminder': reminder_input
									}
									print(f"   📝 Записано в sent_reminders_today")
								else:
									print(f"   ❌ Не удалось отправить")
							
							else:
								# Тихо пропускаем, если не время
								pass
						
						except Exception as e:
							print(f"   ⚠️ Строка {line_num}: ошибка времени: {e}")
							continue
					
					except Exception as e:
						print(f"   ⚠️ Строка {line_num}: ошибка: {e}")
						continue
		
		except Exception as e:
			print(f"💾 Ошибка чтения файла: {e}")
	
	except Exception as e:
		print(f"💥 Ошибка в update_reminder: {e}")
		import traceback
		traceback.print_exc()


def clean_old_reminders():
	"""Очищает старые записи о напоминаниях"""
	try:
		current_date = datetime.now().strftime("%Y-%m-%d")
		cleaned_count = 0
		
		# Очищаем sent_reminders_today (оставляем только сегодняшние)
		old_keys = []
		for key in config.sent_reminders_today:
			parts = key.split('_')
			if len(parts) >= 4 and parts[-1] != current_date:
				old_keys.append(key)
		
		for key in old_keys:
			config.sent_reminders_today.pop(key, None)
			cleaned_count += 1
		
		# Очищаем старые completed_reminders (старше 3 дней)
		three_days_ago = (datetime.now() - time.time() * 3).strftime("%Y-%m-%d")
		for user_id in list(config.completed_reminders.keys()):
			valid_reminders = []
			for reminder in config.completed_reminders[user_id]:
				if reminder['date'] >= three_days_ago:
					valid_reminders.append(reminder)
				else:
					cleaned_count += 1
			
			if valid_reminders:
				config.completed_reminders[user_id] = valid_reminders
			else:
				config.completed_reminders.pop(user_id, None)
		
		if cleaned_count > 0:
			print(f"🧹 Очищено {cleaned_count} старых записей")
	
	except Exception as e:
		print(f"⚠️ Ошибка при очистке: {e}")


def update_cache():
	"""Обновление кэша данных - проверяет дни рождения"""
	print(f"\n🔄 [update_cache] Запуск проверки дней рождения")
	
	try:
		today = datetime.now()
		current_day = today.day
		current_month = today.month
		current_date_str = today.strftime("%Y-%m-%d")
		
		print(f"📅 Сегодня: {current_day}.{current_month} ({current_date_str})")
		
		# Проверяем существует ли файл
		try:
			with open(BIRTHDAY_FILE, 'r', encoding='utf-8') as test_file:
				lines = test_file.readlines()
				print(f"📁 Файл дней рождения найден. Строк: {len(lines)}")
		except FileNotFoundError:
			print(f"❌ Файл {BIRTHDAY_FILE} не найден!")
			return
		
		found_today = 0
		
		with open(BIRTHDAY_FILE, 'r', encoding='utf-8') as file:
			for line_num, line in enumerate(file, 1):
				line = line.strip()
				if not line:
					continue
				
				parts = line.split(maxsplit=2)
				if len(parts) != 3:
					continue
				
				user_id, date_str, full_name = parts
				
				# Пропускаем если уже поздравляли сегодня
				if user_id in config.already_congratulated_today:
					print(f"   ✅ Уже поздравляли сегодня {user_id}")
					continue
				
				try:
					date_clean = date_str.replace(',', '.').strip()
					date_parts = date_clean.split('.')
					
					if len(date_parts) >= 2:
						day_num = int(date_parts[0])
						month_num = int(date_parts[1])
						
						if day_num == current_day and month_num == current_month:
							print(f"   🎉 ДР у {full_name}!")
							found_today += 1
							
							if send_birthday_congrats(user_id, full_name):
								config.already_congratulated_today[user_id] = {
									'name': full_name,
									'date': current_date_str
								}
								print(f"   ✅ Добавлено в очередь")
				
				except Exception:
					continue
		
		print(f"🎯 Найдено дней рождения сегодня: {found_today}")
		
		if found_today == 0:
			print("📭 Сегодня нет дней рождения")
		
		config.last_update = datetime.now()
		print(f"🕒 Проверка завершена: {config.last_update.strftime('%H:%M:%S')}")
	
	except Exception as e:
		print(f"❌ Ошибка в update_cache: {e}")
		import traceback
		traceback.print_exc()


def auto_update_worker():
	"""Фоновая задача для автообновления"""
	
	while True:
		try:
			# Сбрасываем состояния при смене дня
			config.reset_daily_states()
			
			# Очищаем старые записи
			clean_old_reminders()
			
			# Проверяем напоминания
			update_reminder()
			
			# Проверяем дни рождения
			update_cache()
			
			print(f"⏳ Следующая проверка через {config.update_interval} сек...")
			time.sleep(config.update_interval)
		
		except Exception as e:
			print(f"💥 Ошибка в worker: {e}")
			time.sleep(10)


def start_background_worker():
	"""Запускает фоновый worker"""
	print("🚀 [start_background_worker] Запускаю worker...")
	
	try:
		thread = threading.Thread(target=auto_update_worker, daemon=True)
		thread.start()
		print(f"✅ Фоновый worker запущен (проверка каждые {config.update_interval} сек)")
		return thread
	except Exception as e:
		print(f"❌ Не удалось запустить worker: {e}")
		return None
def postpone_reminder(user_id, reminder_text, minutes=10):
    """Создаёт новое напоминание через несколько минут."""
    from datetime import datetime, timedelta
    from config import REMINDER_FILE

    new_time = (datetime.now() + timedelta(minutes=minutes)).strftime("%H:%M")

    with open(REMINDER_FILE, "a", encoding="utf-8") as file:
        file.write(f"{user_id} {new_time} {reminder_text}\n")

    return new_time