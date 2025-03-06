import os

def is_user_allowed(chat_id) -> bool:
    '''
    Проверяем, что сообщение пришло из разрешенной группы
    return: bool
    '''
    ALLOWED_GROUP_CHAT_ID = int(os.getenv('ALLOWED_GROUP_CHAT_ID'))
    return chat_id == ALLOWED_GROUP_CHAT_ID