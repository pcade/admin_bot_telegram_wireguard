from dotenv import load_dotenv
import os
import telebot
from modules.handlers import setup_handlers
from modules.states import user_states, user_data

load_dotenv()

token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)

# Инициализация обработчиков
setup_handlers(bot, user_states, user_data)

bot.infinity_polling()