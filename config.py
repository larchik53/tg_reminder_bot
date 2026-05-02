import telebot
from queue import Queue
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# Очереди для сообщений
message_queue = Queue()  # Для дней рождения
message_queue_reminder = Queue()  # Для напоминаний

# Файлы
REMINDER_FILE = 'reminder.txt'
BIRTHDAY_FILE = 'birthday_fail.txt'

# Состояния
update_interval = 30  # Увеличил интервал до 30 секунд

# Отправленные напоминания сегодня (чтобы не дублировать)
sent_reminders_today = {}  # {key: data}

# Выполненные напоминания
completed_reminders = {}  # {user_id: [list of completed reminders]}

# Уже поздравленные сегодня
already_congratulated_today = {}  # {user_id: data}


# Последнее напоминание для каждого пользователя (чтобы знать, что отмечать как выполненное)
last_reminder_for_user = {}  # {user_id: reminder_text}

# Последнее обновление
last_update = None


def reset_daily_states():
    """Сбрасывает дневные состояния при смене дня"""
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # Проверяем сменился ли день
    if hasattr(reset_daily_states, 'last_date') and reset_daily_states.last_date != today_str:
        print(f"🔄 Новый день! Сбрасываю состояния...")
        
        # Очищаем только если сменился день
        sent_reminders_today.clear()
        already_congratulated_today.clear()
        
        print(f"   Очищено: sent_reminders_today и already_congratulated_today")
    
    reset_daily_states.last_date = today_str


if __name__ == "__main__":
    print("⚠️ Запускать config.py напрямую не нужно!")
    print("Используйте: python main.py")