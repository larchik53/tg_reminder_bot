from config import bot, message_queue, message_queue_reminder
import handlers
import time
from threading import Thread
import sys

from functions import start_background_worker


def process_birthday_queue():
    """
    Отправляет сообщения о днях рождения из очереди.
    """
    while not message_queue.empty():
        try:
            msg = message_queue.get_nowait()

            bot.send_message(
                msg["user_id"],
                msg["text"],
                parse_mode="Markdown"
            )

        except Exception as e:
            print(f"Ошибка отправки дня рождения: {e}")


def process_reminder_queue():
    """
    Отправляет напоминания из очереди.
    После отправки показывает кнопки (сделано / не сделано).
    """
    while not message_queue_reminder.empty():
        try:
            msg = message_queue_reminder.get_nowait()

            # Сохраняем последнее напоминание пользователя
            # чтобы потом можно было отметить его как выполненное
            from config import last_reminder_for_user

            if "reminder_input" in msg:
                last_reminder_for_user[msg["user_id"]] = msg["reminder_input"]

            bot.send_message(
                msg["user_id"],
                msg["text"],
                parse_mode="Markdown"
            )

            # Показываем кнопки после отправки напоминания
            from handlers import add_function_reminder
            add_function_reminder(msg["user_id"])

        except Exception as e:
            print(f"Ошибка отправки напоминания: {e}")


def polling_thread():
    """
    Запускает polling Telegram в отдельном потоке.
    """
    try:
        bot.polling(none_stop=True, interval=1, timeout=10)

    except Exception as e:
        print(f"Ошибка polling: {e}")


if __name__ == "__main__":
    print("Запуск бота...")

    # Запускаем фоновую проверку напоминаний
    start_background_worker()

    # Запускаем Telegram polling в отдельном потоке
    poll_thread = Thread(target=polling_thread, daemon=True)
    poll_thread.start()

    print("Бот запущен. Для остановки нажмите Ctrl+C")

    try:
        while True:
            # Обрабатываем очереди сообщений
            process_birthday_queue()
            process_reminder_queue()

            time.sleep(2)

    except KeyboardInterrupt:
        print("Бот остановлен пользователем")
        sys.exit(0)

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)
        
        secrution.py
        time_rezerv_betta.py
        text_time_menedger
        reminder