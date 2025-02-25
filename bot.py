from dotenv import load_dotenv
import os
import telebot
from telebot import types
load_dotenv()

token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)

# Замените на chat ID вашей группы
ALLOWED_GROUP_CHAT_ID = int(os.getenv('ALLOWED_GROUP_CHAT_ID'))

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
config_name = types.KeyboardButton("NAME")
config_ip = types.KeyboardButton("IP")
config_date = types.KeyboardButton("DATE")
config_comment = types.KeyboardButton("COMMENT")
config_clear = types.KeyboardButton("CLEAR")
config_show = types.KeyboardButton("SHOW")
config_create = types.KeyboardButton("CREATE")
menu.add(config_name, config_ip, config_date, config_comment, config_clear, config_show, config_create)

def is_user_allowed(chat_id):
    # Проверяем, что сообщение пришло из разрешенной группы
    return chat_id == ALLOWED_GROUP_CHAT_ID

@bot.message_handler(commands=['start'])
def start_message(message):
    if not is_user_allowed(message.chat.id):
        bot.send_message(message.chat.id, "Извините, у вас нет доступа к этому боту.")
        return
    
    bot.send_message(message.chat.id, "Привет ✌️", reply_markup=menu)

# Словарь для хранения состояний пользователей
user_states = {}
# Словарь для хранения введённых данных
user_data = {}

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    
    if not is_user_allowed(chat_id):
        return  # Игнорируем сообщения из других чатов
    
    # Обработка сообщений из разрешенной группы
    if message.text == "NAME":
        bot.send_message(chat_id, "Введите имя для конфигурации", reply_markup=menu)
        user_states[chat_id] = 'waiting_for_name_input'  # Устанавливаем состояние ожидания ввода имени
    elif message.text == "IP":
        bot.send_message(chat_id, "Введите IP для конфигурации", reply_markup=menu)
        user_states[chat_id] = 'waiting_for_ip_input'  # Устанавливаем состояние ожидания ввода IP
    elif message.text == "DATE":
        bot.send_message(chat_id, "Введите дату окончания подписки", reply_markup=menu)
        user_states[chat_id] = 'waiting_for_date_input'  # Устанавливаем состояние ожидания ввода даты
    elif message.text == "COMMENT":
        bot.send_message(chat_id, "Введите комментарий для конфигурации", reply_markup=menu)
        user_states[chat_id] = 'waiting_for_comment_input'  # Устанавливаем состояние ожидания ввода комментария
    elif message.text == "SHOW":
        if chat_id in user_data:
            config_name = user_data[chat_id].get('config_name', 'не указано')
            ip = user_data[chat_id].get('ip', 'не указано')
            date = user_data[chat_id].get('date', 'не указано')
            comment = user_data[chat_id].get('comment', 'не указано')
            bot.send_message(chat_id, f"Вы ввели:\nИмя: {config_name}\nIP: {ip}\nДата: {date}\nКомментарий: {comment}", reply_markup=menu)
            #user_data.pop(chat_id)  # Очищаем данные пользователя после вывода
        else:
            bot.send_message(chat_id, "Вы ещё не ввели данные для конфигурации.", reply_markup=menu)
    elif message.text == "CLEAR":
        if chat_id in user_data:
            user_data.pop(chat_id)
            bot.send_message(chat_id, "Все введенные данные очищены.", reply_markup=menu)
        else:
            bot.send_message(chat_id, "Нет данных для очистки.", reply_markup=menu)
    else:
        # Обработка ввода данных в зависимости от текущего состояния
        if chat_id in user_states:
            # Инициализация словаря для пользователя, если его ещё нет
            if chat_id not in user_data:
                user_data[chat_id] = {}
            
            if user_states[chat_id] == 'waiting_for_name_input':
                user_data[chat_id]['config_name'] = message.text
                bot.send_message(chat_id, f"Имя '{message.text}' сохранено.", reply_markup=menu)
            elif user_states[chat_id] == 'waiting_for_ip_input':
                user_data[chat_id]['ip'] = message.text
                bot.send_message(chat_id, f"IP '{message.text}' сохранён.", reply_markup=menu)
            elif user_states[chat_id] == 'waiting_for_date_input':
                user_data[chat_id]['date'] = message.text
                bot.send_message(chat_id, f"Дата '{message.text}' сохранена.", reply_markup=menu)
            elif user_states[chat_id] == 'waiting_for_comment_input':
                user_data[chat_id]['comment'] = message.text
                bot.send_message(chat_id, f"Комментарий '{message.text}' сохранён.", reply_markup=menu)
            user_states[chat_id] = None  # Сбрасываем состояние после сохранения данных

bot.infinity_polling()