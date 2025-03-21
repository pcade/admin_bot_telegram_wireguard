from telebot import types
from telebot import TeleBot
from typing import Any
from modules.states import UserStates
from modules.common import is_user_allowed,  validate_ip, is_ascii, ip_is_free
from modules.commands import *

def create_menu_keyboard() -> types.ReplyKeyboardMarkup:
    """
    Создает и возвращает клавиатуру меню с кнопками.

    :return: Клавиатура с кнопками меню. (types.ReplyKeyboardMarkup)
    """
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["NAME",
               "IP",
               "DATE",
               "COMMENT",
               "REMOVE",
               "CLEAR",
               "SHOW",
               "CREATE",
               "CONFIG"]

    # Добавляем все кнопки в одну строку
    menu.add(*[types.KeyboardButton(button) for button in buttons])

    return menu

def setup_handlers(bot: TeleBot, user_states: dict) -> None:
    """
    Настраивает обработчики сообщений для бота.

    :param bot: Объект бота (object.TeleBot)
    :param user_states: Объект для хранения состояний пользователей (dict)
    :return: None
    """
    menu_keyboard = create_menu_keyboard()

    @bot.message_handler(commands=['start'])
    def start(message: Any) -> None:
        """
        Обработчик команды /start.

        :param message: Сообщение от пользователя (object)
        :return: None
        """
        if not is_user_allowed(message.chat.id):
            send_access_denied_message(bot, message)
            return
        bot.send_message(message.chat.id,
                         "Привет! 👋",
                         reply_markup=menu_keyboard)

    @bot.message_handler(func=lambda message: True)
    def handle_all_messages(message: Any) -> None:
        """
        Обработчик всех сообщений.

        :param message: Сообщение от пользователя (object)
        :return: None
        """
        if not is_user_allowed(message.chat.id):
            return

        if message.text in ["NAME", "IP", "DATE", "COMMENT"]:
            handle_input_request(bot,
                                 message.chat.id,
                                 message.text,
                                 user_states,
                                 menu_keyboard)
        elif message.text == "SHOW":
            handle_show_request(bot,
                                message.chat.id,
                                user_states,
                                menu_keyboard)
        elif message.text == "CLEAR":
            handle_clear_request(bot,
                                 message.chat.id,
                                 user_states,
                                 menu_keyboard)
        elif message.text == "CREATE":
            handle_create_request(bot,
                                  message.chat.id,
                                  user_states,
                                  menu_keyboard)
        elif message.text == "CONFIG":
            handle_show_config_ips(bot,
                                   message.chat.id,
                                   menu_keyboard)
        elif message.text == "REMOVE":
            handle_remove_by_ip_from_config(bot,
                                   message.chat.id,
                                   user_states,
                                   menu_keyboard)
        else:
            handle_user_input(bot,
                              message.chat.id,
                              message.text,
                              user_states,
                              menu_keyboard)

def send_access_denied_message(bot: TeleBot, message: Any) -> None:
    """
    Отправляет сообщение о запрете доступа.

    :param bot: Объект бота (object.TeleBot)
    :param message: Сообщение от пользователя (object)
    :return: None
    """
    bot.send_message(
        message.chat.id,
        text="💀💀💀💀\nuser - {0.username}\nid - {0.id}\n{0.first_name} {0.last_name}\nNo rule\n💀💀💀💀".format(message.from_user)
    )

def handle_input_request(bot: TeleBot, chat_id: int, input_type: str, user_states: dict, menu_keyboard: Any) -> None:
    """
    Обрабатывает сообщение пользователя и вызывает соответствующие функции.

    :param bot: Объект бота (object.TeleBot)
    :param chat_id: ID чата (int)
    :param input_type: Ключ (str)
    :param user_states: Объект для хранения состояний пользователей (dict)
    :param menu_keyboard: Клавиатура меню (Any)
    :return: None
    """
    prompts = {
        "NAME": "Введите имя для конфигурации",
        "IP": "Введите IP для конфигурации",
        "DATE": "Введите дату окончания подписки",
        "COMMENT": "Введите комментарий для конфигурации"
    }
    bot.send_message(chat_id,
                     prompts[input_type],
                     reply_markup=menu_keyboard)
    user_states.set_user_state(chat_id,
                               f"waiting_for_{input_type.lower()}_input")

def handle_show_request(bot: TeleBot, chat_id: int, user_states: dict, menu_keyboard: Any) -> None:
    """
    Показывает введенные данные.

    :param bot: Объект бота (object.TeleBot)
    :param chat_id: ID чата (int)
    :param user_states: Объект для хранения состояний пользователей (dict)
    :param menu_keyboard: Клавиатура меню (Any)
    :return: None
    """
    user_data: dict[str,str] = user_states.get_user_data(chat_id)

    response: str = (
        f"Вы ввели:\n"
        f"Имя: {user_data.get('name', '')}\n"
        f"IP: {user_data.get('ip', '')}\n"
        f"Дата: {user_data.get('date', '')}\n"
        f"Комментарий: {user_data.get('comment', '')}"
    )
    bot.send_message(chat_id,
                     response,
                     reply_markup=menu_keyboard)

def handle_clear_request(bot: TeleBot, chat_id: int, user_states: dict, menu_keyboard: Any) -> None:
    """
    Очищает данные пользователя.

    :param bot: Объект бота (object.TeleBot)
    :param chat_id: ID чата (int)
    :param user_states: Объект для хранения состояний пользователей (dict)
    :param menu_keyboard: Клавиатура меню (Any)
    :return: None
    """
    user_states.clear_user_data(chat_id)
    user_states.clear_user_state(chat_id)
    bot.send_message(chat_id,
                     "Данные очищены.",
                     reply_markup=menu_keyboard)

def handle_create_request(bot: TeleBot, chat_id: int, user_states: dict, menu_keyboard: Any) -> None:
    """
    Создает конфигурацию и отправляет файлы.

    :param bot: Объект бота (object.TeleBot)
    :param chat_id: ID чата (int)
    :param user_states: Объект для хранения состояний пользователей (dict)
    :param menu_keyboard: Клавиатура меню (Any)
    :return: None
    """
    user_data: dict[str,str] = user_states.get_user_data(chat_id)
    usr_name: str = user_data.get('name', '')
    usr_ip: str = user_data.get('ip', '')
    usr_comment: str = user_data.get('comment', '')
    usr_date: str = user_data.get('date', '')
    if not user_data:
        bot.send_message(chat_id,
                         "Сначала введите данные.",
                         reply_markup=menu_keyboard)
        return

    try:
        config_path: str
        qr_path: str
        config_path, qr_path = generate_configuration(usr_name, usr_ip, usr_comment, usr_date)
        send_configuration_files(bot,
                                 chat_id,
                                 config_path,
                                 qr_path)
        bot.send_message(chat_id,
                         "Конфигурация успешно создана!",
                         reply_markup=menu_keyboard)

        remove_configuration_files(usr_name) # удаляем конфигурационные файлы
        daemon_reload() # перезапускаем демонов

    except Exception as e:
        bot.send_message(chat_id,
                         f"Ошибка: {e}",
                         reply_markup=menu_keyboard)

def handle_remove_by_ip_from_config(bot: TeleBot, chat_id: int, user_states: dict, menu_keyboard: Any) -> None:
    """
    Создает конфигурацию и отправляет файлы.

    :param bot: Объект бота (object.TeleBot)
    :param chat_id: ID чата (int)
    :param user_states: Объект для хранения состояний пользователей (dict)
    :param menu_keyboard: Клавиатура меню (Any)
    :return: None
    """
    user_data: dict[str,str] = user_states.get_user_data(chat_id)
    usr_ip: str = user_data.get('ip', '')
    if not user_data:
        bot.send_message(chat_id,
                         "Сначала введите данные.",
                         reply_markup=menu_keyboard)
        return

    try:
        bot.send_message(chat_id,
                         "Конфигурация успешно удалена!",
                         reply_markup=menu_keyboard)

        remove_configuration(usr_ip)
    
        daemon_reload() # перезапускаем демонов

    except Exception as e:
        bot.send_message(chat_id,
                         f"Ошибка: {e}",
                         reply_markup=menu_keyboard)


def handle_show_config_ips(bot: TeleBot, chat_id: int, menu_keyboard: Any) -> None:
    """
    Создает конфигурацию и отправляет файлы.

    :param bot: Объект бота (object.TeleBot)
    :param chat_id: ID чата (int)
    :param user_states: Объект для хранения состояний пользователей (dict)
    :param menu_keyboard: Клавиатура меню (Any)
    :return: None
    """
    try:
        data: str = json.loads(show_config_ips())
        formatted_output = format_peer_info(data)
        
        # Лимит символов для одного сообщения в Telegram
        max_message_length = 4096
        
        # Разбиваем сообщение на части, если оно превышает лимит
        messages = [formatted_output[i:i + max_message_length] for i in range(0, len(formatted_output), max_message_length)]
        
        # Отправляем каждую часть сообщения
        for message in messages:
            bot.send_message(chat_id,
                             f"На данный момент используются {message}",
                             reply_markup=menu_keyboard)
    except Exception as e:
        bot.send_message(chat_id,
                         f"Ошибка: {e}",
                         reply_markup=menu_keyboard)

def handle_user_input(bot: TeleBot, chat_id: int, text: str, user_states: dict, menu_keyboard: Any) -> None:
    """
    Обрабатывает ввод пользователя.

    :param bot: Объект бота (object.TeleBot)
    :param chat_id: ID чата (int)
    :param text: Текст сообщения (str)
    :param user_states: Объект для хранения состояний пользователей (dict)
    :param menu_keyboard: Клавиатура меню (Any)
    :return: None
    """
    state: str = user_states.get_user_state(chat_id)
    if state:
        key: str = state.replace("waiting_for_", "").replace("_input", "")
        
        # Валидация данных
        if key == "name" and not is_ascii(text):
            bot.send_message(chat_id,
                             "Имя должно содержать только ASCII символы.",
                             reply_markup=menu_keyboard)
            return
        elif key == "ip":
            if not validate_ip(text):
                bot.send_message(chat_id,
                                 "Некорректный IP-адрес.",
                                 reply_markup=menu_keyboard)
                return
            if not ip_is_free(text):
                bot.send_message(chat_id,
                     "IP-адрес занят.",
                     reply_markup=menu_keyboard)
        elif key == "date":
            pass
        elif key == "comment" and not is_ascii(text):
            pass

        user_states.update_user_data(chat_id, key, text)
        bot.send_message(chat_id,
                         f"{key.capitalize().lower()} '{text}' сохранено.",
                         reply_markup=menu_keyboard)
        user_states.clear_user_state(chat_id)