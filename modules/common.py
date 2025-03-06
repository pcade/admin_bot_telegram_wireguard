import os
import ipaddress

def is_user_allowed(chat_id) -> bool:
    '''
    Проверяем, что сообщение пришло из разрешенной группы

    :param chat_id: (int)
    :return: (bool)
    '''
    ALLOWED_GROUP_CHAT_ID: int = int(os.getenv('ALLOWED_GROUP_CHAT_ID'))
    return chat_id == ALLOWED_GROUP_CHAT_ID

def validate_ip(ip) -> bool:
    '''
    Проверяет, является ли строка корректным IP-адресом.

    :param ip: (str)
    :return: (bool)
    '''
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_ascii(s) -> bool:
    '''
    Проверяет, состоит ли строка только из символов ASCII.

    :param s: (str)
    :return: (bool)
    '''
    if all(ord(c) < 128 for c in s):
        return True
    else:
        return False