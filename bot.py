from dotenv import load_dotenv
import os
import telebot
from modules.handlers import setup_handlers
from modules.states import UserStates

# Загрузка переменных окружения
load_dotenv()

# Инициализация бота
TELEGRAM_TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Инициализация состояний пользователей
user_states = UserStates()

# Настройка обработчиков
setup_handlers(bot, user_states)

# Запуск бота
bot.infinity_polling()