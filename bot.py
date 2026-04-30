# main.py
from config import bot, message_queue, message_queue_reminder
import handlers
import time
from threading import Thread
import sys

print("=" * 50)
print("🤖 ЗАПУСК БОТА")
print("=" * 50)

# Импортируем ПОСЛЕ config
from functions import start_background_worker


def process_birthday_queue():
	"""Обрабатывает очередь сообщений о днях рождения"""
	if not message_queue.empty():
		print(f"📦 В очереди дней рождения: {message_queue.qsize()} сообщений")
		
		while not message_queue.empty():
			try:
				msg = message_queue.get_nowait()
				print(f"   📨 Отправляю {msg['user_id']}: {msg['text'][:30]}...")
				
				bot.send_message(msg['user_id'], msg['text'], parse_mode='Markdown')
				print(f"   ✅ Отправлено!")
			
			except Exception as e:
				print(f"   ❌ Ошибка отправки дня рождения: {e}")
	else:
		print("   📭 Очередь дней рождения пуста")


def process_reminder_queue():
	"""Обрабатывает очередь напоминаний"""
	if not message_queue_reminder.empty():
		print(f"📦 В очереди напоминаний: {message_queue_reminder.qsize()} сообщений")
		
		while not message_queue_reminder.empty():
			try:
				msg = message_queue_reminder.get_nowait()
				print(f"   📨 Отправляю напоминание {msg['user_id']}: {msg['text'][:30]}...")
				
				# Сохраняем текст напоминания для этого пользователя
				from config import last_reminder_for_user
				if 'reminder_input' in msg:
					last_reminder_for_user[msg['user_id']] = msg['reminder_input']
					print(f"   📝 Сохранено напоминание для пользователя {msg['user_id']}")
				
				# Отправляем напоминание
				bot.send_message(msg['user_id'], msg['text'], parse_mode='Markdown')
				
				# После отправки показываем меню выбора
				from handlers import add_function_reminder
				add_function_reminder(msg['user_id'])
				
				print(f"   ✅ Напоминание отправлено!")
			
			except Exception as e:
				print(f"   ❌ Ошибка отправки напоминания: {e}")
	else:
		print("   📭 Очередь напоминаний пуста")


def polling_thread():
	"""Отдельный поток для polling бота"""
	print("🔁 Запуск polling в отдельном потоке...")
	
	try:
		bot.polling(none_stop=True, interval=1, timeout=10)
	except Exception as e:
		print(f"💥 Критическая ошибка в polling потоке: {e}")
		import traceback
		traceback.print_exc()


if __name__ == "__main__":
	print("1. Запускаю фоновый worker для проверки дней рождения и напоминаний...")
	worker_thread = start_background_worker()
	
	print("\n2. Запускаю поток для polling бота...")
	poll_thread = Thread(target=polling_thread, daemon=True)
	poll_thread.start()
	
	print("\n3. Запускаю обработку очередей...")
	print("   Для остановки: Ctrl+C")
	print("-" * 50)
	
	try:
		while True:
			try:
				process_birthday_queue()
				process_reminder_queue()
				
				time.sleep(2)
			
			except Exception as e:
				print(f"⚠️ Ошибка в основном цикле: {e}")
				time.sleep(5)
	
	except KeyboardInterrupt:
		print("\n\n⏹️ Остановлено пользователем")
		print("👋 До свидания!")
		sys.exit(0)
	
	except Exception as e:
		print(f"\n💥 Критическая ошибка: {e}")
		import traceback
		
		traceback.print_exc()
		sys.exit(1)