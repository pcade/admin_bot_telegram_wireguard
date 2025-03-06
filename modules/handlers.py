from telebot import types
from modules.states import UserStates
from modules.common import is_user_allowed
from modules.commands import generate_configuration, send_configuration_files

def create_menu_keyboard() -> types.ReplyKeyboardMarkup:
    """
    Создает и возвращает клавиатуру меню с кнопками.

    return:
        types.ReplyKeyboardMarkup: Клавиатура с кнопками меню.
    """
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["NAME", "IP", "DATE", "COMMENT", "CLEAR", "SHOW", "CREATE"]

    # Добавляем все кнопки в одну строку
    menu.add(*[types.KeyboardButton(button) for button in buttons])

    return menu

def setup_handlers(bot, user_states):
    """
    Настраивает обработчики сообщений для бота.
    """
    menu_keyboard = create_menu_keyboard()

    @bot.message_handler(commands=['start'])
    def start(message):
        """
        Обработчик команды /start.
        """
        if not is_user_allowed(message.chat.id):
            send_access_denied_message(bot, message)
            return
        bot.send_message(message.chat.id, "Привет! 👋", reply_markup=menu_keyboard)

    @bot.message_handler(func=lambda message: True)
    def handle_all_messages(message):
        """
        Обработчик сообщений.
        """
        chat_id = message.chat.id

        if not is_user_allowed(chat_id):
            return

        if message.text in ["NAME", "IP", "DATE", "COMMENT"]:
            handle_input_request(bot, chat_id, message.text, user_states, menu_keyboard)
        elif message.text == "SHOW":
            handle_show_request(bot, chat_id, user_states, menu_keyboard)
        elif message.text == "CLEAR":
            handle_clear_request(bot, chat_id, user_states, menu_keyboard)
        elif message.text == "CREATE":
            handle_create_request(bot, chat_id, user_states, menu_keyboard)
        else:
            handle_user_input(bot, chat_id, message.text, user_states, menu_keyboard)

def send_access_denied_message(bot, message):
    """
    Отправляет сообщение о запрете доступа.
    """
    bot.send_message(
        message.chat.id,
        text="💀💀💀💀\nuser - {0.username}\nid - {0.id}\n{0.first_name} {0.last_name}\nNo rule\n💀💀💀💀".format(message.from_user)
    )

def handle_input_request(bot, chat_id, input_type, user_states, menu_keyboard):
    """
    Обрабатывает запросы на ввод данных.
    """
    prompts = {
        "NAME": "Введите имя для конфигурации",
        "IP": "Введите IP для конфигурации",
        "DATE": "Введите дату окончания подписки",
        "COMMENT": "Введите комментарий для конфигурации"
    }
    bot.send_message(chat_id, prompts[input_type], reply_markup=menu_keyboard)
    user_states.set_user_state(chat_id, f"waiting_for_{input_type.lower()}_input")

def handle_show_request(bot, chat_id, user_states, menu_keyboard):
    """
    Показывает введенные данные.
    """
    user_data = user_states.get_user_data(chat_id)

    response = (
        f"Вы ввели:\n"
        f"Имя: {user_data.get('name', '')}\n"
        f"IP: {user_data.get('ip', '')}\n"
        f"Дата: {user_data.get('date', '')}\n"
        f"Комментарий: {user_data.get('comment', '')}"
    )
    bot.send_message(chat_id, response, reply_markup=menu_keyboard)

def handle_clear_request(bot, chat_id, user_states, menu_keyboard):
    """
    Очищает данные пользователя.
    """
    user_states.clear_user_data(chat_id)
    user_states.clear_user_state(chat_id)
    bot.send_message(chat_id, "Данные очищены.", reply_markup=menu_keyboard)

def handle_create_request(bot, chat_id, user_states, menu_keyboard):
    """
    Создает конфигурацию и отправляет файлы.
    """
    user_data = user_states.get_user_data(chat_id)
    usr_name = user_data.get('name', '')
    usr_ip = user_data.get('ip', '')
    usr_comment = user_data.get('comment', '')
    usr_date = user_data.get('date', '')
    if not user_data:
        bot.send_message(chat_id, "Сначала введите данные.", reply_markup=menu_keyboard)
        return

    try:
        config_path, qr_path = generate_configuration(usr_name, usr_ip, usr_comment)
        send_configuration_files(bot, chat_id, config_path, qr_path)
        bot.send_message(chat_id, "Конфигурация успешно создана!", reply_markup=menu_keyboard)
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка: {e}", reply_markup=menu_keyboard)

def handle_user_input(bot, chat_id, text, user_states, menu_keyboard):
    """
    Обрабатывает ввод пользователя.
    """
    state = user_states.get_user_state(chat_id)
    if state:
        key = state.replace("waiting_for_", "").replace("_input", "")
        user_states.update_user_data(chat_id, key, text)
        bot.send_message(chat_id, f"{key.capitalize().lower()} '{text}' сохранено.", reply_markup=menu_keyboard)
        user_states.clear_user_state(chat_id)