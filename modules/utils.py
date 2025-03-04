import os

def is_user_allowed(chat_id) -> int:
    '''
    Проверяем, что сообщение пришло из разрешенной группы
    return: int
    '''
    ALLOWED_GROUP_CHAT_ID = int(os.getenv('ALLOWED_GROUP_CHAT_ID'))
    return chat_id == ALLOWED_GROUP_CHAT_ID