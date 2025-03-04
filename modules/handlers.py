from telebot import types
from modules.states import user_states, user_data
from modules.utils import is_user_allowed
from modules.commands import handle_create_request
from telebot import types

# Создаем клавиатуру
menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
config_name = types.KeyboardButton("NAME")
config_ip = types.KeyboardButton("IP")
config_date = types.KeyboardButton("DATE")
config_comment = types.KeyboardButton("COMMENT")
config_clear = types.KeyboardButton("CLEAR")
config_show = types.KeyboardButton("SHOW")
config_create = types.KeyboardButton("CREATE")
menu.add(config_name, config_ip, config_date, config_comment, config_clear, config_show, config_create)

def setup_handlers(bot, user_states, user_data):
    @bot.message_handler(commands=['start'])
    def start(message):
        if not is_user_allowed(message.chat.id):
            bot.send_message(message.chat.id,
            text="💀💀💀💀\nuser - {0.username}\nid - {0.id}\n{0.first_name} {0.last_name}\nNo rule\n💀💀💀💀".format(message.from_user))
            return
        
        bot.send_message(message.chat.id, "Привет ✌️", reply_markup=menu)

    @bot.message_handler(func=lambda message: True)
    def handle_all_messages(message):
        chat_id = message.chat.id

        if not is_user_allowed(chat_id):
            return  # Игнорируем сообщения из других чатов
        
        if message.text in ["NAME", "IP", "DATE", "COMMENT"]:
            handle_input_requests(message)
        elif message.text == "SHOW":
            handle_show_request(chat_id)
        elif message.text == "CLEAR":
            handle_clear_request(chat_id)
        elif message.text == "CREATE":
            handle_create_request(chat_id)
        else:
            handle_user_input(chat_id, message.text)

    def handle_input_requests(message):
        chat_id = message.chat.id
        if message.text == "NAME":
            bot.send_message(chat_id, "Введите имя для конфигурации", reply_markup=menu)
            user_states[chat_id] = 'waiting_for_name_input'
        elif message.text == "IP":
            bot.send_message(chat_id, "Введите IP для конфигурации", reply_markup=menu)
            user_states[chat_id] = 'waiting_for_ip_input'
        elif message.text == "DATE":
            bot.send_message(chat_id, "Введите дату окончания подписки", reply_markup=menu)
            user_states[chat_id] = 'waiting_for_date_input'
        elif message.text == "COMMENT":
            bot.send_message(chat_id, "Введите комментарий для конфигурации", reply_markup=menu)
            user_states[chat_id] = 'waiting_for_comment_input'

    def handle_show_request(chat_id):
        if chat_id in user_data:
            config_name = user_data[chat_id].get('config_name', '')
            ip = user_data[chat_id].get('ip', '')
            date = user_data[chat_id].get('date', '')
            comment = user_data[chat_id].get('comment', '')
            bot.send_message(chat_id, f"Вы ввели:\nИмя: {config_name}\nIP: {ip}\nДата: {date}\nКомментарий: {comment}\n{user_data}", reply_markup=menu)
        else:
            user_data[chat_id] = {chat_id:{'config_name': '', 'ip': '', 'date': '', 'comment': ''}}
            bot.send_message(chat_id, f"Вы ещё не ввели данные для конфигурации.{user_data}", reply_markup=menu)

    def handle_clear_request(chat_id):
        if chat_id in user_data:
            user_data.pop(chat_id)
            bot.send_message(chat_id, "Все введенные данные очищены.", reply_markup=menu)
        else:
            bot.send_message(chat_id, "Нет данных для очистки.", reply_markup=menu)

    def handle_user_input(chat_id, text):
        if chat_id in user_states:
            if chat_id not in user_data:
                user_data[chat_id] = {}
            
            if user_states[chat_id] == 'waiting_for_name_input':
                user_data[chat_id]['config_name'] = text
                bot.send_message(chat_id, f"Имя '{text}' сохранено.", reply_markup=menu)
            elif user_states[chat_id] == 'waiting_for_ip_input':
                user_data[chat_id]['ip'] = text
                bot.send_message(chat_id, f"IP '{text}' сохранён.", reply_markup=menu)
            elif user_states[chat_id] == 'waiting_for_date_input':
                user_data[chat_id]['date'] = text
                bot.send_message(chat_id, f"Дата '{text}' сохранена.", reply_markup=menu)
            elif user_states[chat_id] == 'waiting_for_comment_input':
                user_data[chat_id]['comment'] = text
                bot.send_message(chat_id, f"Комментарий '{text}' сохранён.", reply_markup=menu)
            user_states[chat_id] = None  # Сбрасываем состояние после сохранения данных