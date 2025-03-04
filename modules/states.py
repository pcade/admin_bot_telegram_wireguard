class UserStates:
    """Класс для управления состояниями и данными пользователей."""

    def __init__(self):
        self.user_states = {}  # Состояния пользователей
        self.user_data = {}    # Данные пользователей

    def get_user_state(self, chat_id):
        """Возвращает текущее состояние пользователя."""
        return self.user_states.get(chat_id)

    def set_user_state(self, chat_id, state):
        """Устанавливает состояние пользователя."""
        self.user_states[chat_id] = state

    def clear_user_state(self, chat_id):
        """Очищает состояние пользователя."""
        self.user_states.pop(chat_id, None)

    def get_user_data(self, chat_id):
        """Возвращает данные пользователя."""
        return self.user_data.get(chat_id, {})

    def update_user_data(self, chat_id, key, value):
        """Обновляет данные пользователя."""
        if chat_id not in self.user_data:
            self.user_data[chat_id] = {}
        self.user_data[chat_id][key] = value

    def clear_user_data(self, chat_id):
        """Очищает данные пользователя."""
        self.user_data.pop(chat_id, None)