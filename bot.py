from dotenv import load_dotenv
import os
load_dotenv()

token = os.getenv('TOKEN')

import telebot
from telebot import types

bot = telebot.TeleBot(token)

# Замените на chat ID вашей группы
ALLOWED_GROUP_CHAT_ID = int(os.getenv('ALLOWED_GROUP_CHAT_ID'))

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
service = types.KeyboardButton("Услуги")
price = types.KeyboardButton("Цена")
contacts = types.KeyboardButton("Контакты")
adress = types.KeyboardButton("Адреса")
sign_up = types.KeyboardButton("Записаться")
menu.add(service, price, contacts, adress, sign_up)

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button = types.KeyboardButton("Назад")
back.add(back_button)

def is_user_allowed(chat_id):
    # Проверяем, что сообщение пришло из разрешенной группы
    return chat_id == ALLOWED_GROUP_CHAT_ID

@bot.message_handler(commands=['start'])
def start_message(message):
    if not is_user_allowed(message.chat.id):
        bot.send_message(message.chat.id, "Извините, у вас нет доступа к этому боту.")
        return
    
    bot.send_message(message.chat.id, "Привет ✌️", reply_markup=menu)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if not is_user_allowed(message.chat.id):
        return  # Игнорируем сообщения из других чатов
    
    # Обработка сообщений из разрешенной группы
    if message.text == "Услуги":
        bot.send_message(message.chat.id, "Вот наши услуги...", reply_markup=back)
    elif message.text == "Цена":
        bot.send_message(message.chat.id, "Вот наши цены...", reply_markup=back)
    elif message.text == "Контакты":
        bot.send_message(message.chat.id, "Вот наши контакты...", reply_markup=back)
    elif message.text == "Адреса":
        bot.send_message(message.chat.id, "Вот наши адреса...", reply_markup=back)
    elif message.text == "Записаться":
        bot.send_message(message.chat.id, "Записаться можно здесь...", reply_markup=back)
    elif message.text == "Назад":
        bot.send_message(message.chat.id, "Возвращаемся в меню", reply_markup=menu)

bot.infinity_polling()