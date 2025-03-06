# Telegram Bot for WireGuard Configuration
---

## Описание **`/eng`** Description
Этот проект представляет собой Telegram-бота, работающего в **приватном** режиме, который позволяет генерировать конфигурации для WireGuard. Пользователи могут получать конфигурационный файл в виде текстового документа и QR-кода через Telegram. Этот проект является частью проекта автоконфигурации клиентских конфигов Wireguard проекта [WireguardAutoConfiguration](https://github.com/pcade/WireguardAutoConfinguration).
This project is a Telegram bot that operates in **private** mode, allowing users to generate configurations for WireGuard. Users can receive the configuration file as a text document and a QR code via Telegram. This project is part of project autoconfiguration clients config Wireguard [WireguardAutoConfiguration](https://github.com/pcade/WireguardAutoConfinguration).

## Функциональность **`/eng`** Functionality

- Генерация конфигураций WireGuard на основе введенных пользователем данных (имя, IP-адрес, комментарий). **`/eng`** Generation of WireGuard configurations based on user-provided data (name, IP address, comment).
- Отправка сгенерированных конфигурационных файлов и QR-кодов пользователю. **`/eng`** Sending generated configuration files and QR codes to the user.
- Хранение состояний пользователей для управления вводом данных, при этом обеспечивается высокая степень приватности. **`/eng`** Storing user states to manage data input while ensuring a high level of privacy.
- Обработка команд и сообщений от пользователей с соблюдением конфиденциальности данных. **`/eng`** Handling commands and messages from users while maintaining data confidentiality.


## Установка **`/eng`** Installation

1. **Клонируйте репозиторий **`/eng`** Clone the repository:**

   ```bash
   git clone https://github.com/pcade/admin_bot_telegram_wireguard.git
   cd admin_bot_telegram_wireguard
   ```

2. **Создайте виртуальное окружение (рекомендуется) **`/eng`** Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux / For Linux
   ```

3. **Установите зависимости **`/eng`** Install dependencies:**

   ```bash
   sudo pip install -r requirements.txt
   ```

4. **Создайте файл `.env` в корне проекта и добавьте ваш токен Telegram `/eng` Create a `.env` file in the project root and add your Telegram token:**

   ```plaintext
   TOKEN=ваш_токен_телеграм / your_telegram_token
   ALLOWED_GROUP_CHAT_ID="ваш_персональный_id_чата" / your_personal_chat_id
   ```

## Использование  **`/eng`** Usage

1. **Запустите бота `/eng` Start the bot:**

   ```bash
   sudo python bot.py
   ```

2. **Откройте Telegram и найдите вашего бота по имени бота который вы указали при его создании **`/eng`** Open Telegram and find your bot by the bot name you specified when creating it.**
3. Используйте команды:
   - `/start` - Начать взаимодействие с ботом. **`/eng`** `/start` interacting with the bot.
   - Введите `NAME`, `IP`, `DATE`, `COMMENT` для ввода соответствующих данных. **`/eng`** Enter `NAME`, `IP`, `DATE`, `COMMENT` to input the corresponding data.
   - Введите `SHOW` для отображения введенных данных. **`/eng`** Enter `SHOW` to display the entered data.
   - Введите `CLEAR` для очистки данных. **`/eng`** Enter `CLEAR` to clear the data.
   - Введите `CREATE` для создания конфигурации и получения файлов. **`/eng`** Enter `CREATE` to create the configuration and receive the files.

## Структура проекта **`/eng`** Project Structure

```
.
├── bot.py # Основной файл для запуска бота / Main file to run the bot
├── modules # Директория с модулями / Directory with modules
│   ├── commands.py # Выполнения команд связанных с конфигурацией / Command execution related to configuration
│   ├── common.py # Вспомогательные функции / Helper functions
│   ├── handlers.py # Обработчики сообщений / Message handlers
│   └── states.py # Управление состояниями пользователей / User state management
├── README.md # Документация проекта / Project documentation
├── requirements.txt # Список зависимостей / List of dependencies
└── utils # Директория с вспомогательными переменными / Directory with helper variables
    └── utils.py # Вспомогательные переменные / Helper variables
```

## Лицензия **`/eng`** License

Этот проект лицензирован под `MIT License`. Пожалуйста, смотрите файл [LICENSE](LICENSE) для получения дополнительной информации. **`/eng`** This project is licensed under the `MIT License`. Please see the [LICENSE](LICENSE) file for more information.

## Контрибьюция **`/eng`** Contribution

>Если вы хотите внести свой вклад в проект, пожалуйста, создайте форк репозитория и отправьте пулл-реквест с вашими изменениями. **`/eng`** If you would like to contribute to the project, please create a fork of the repository and submit a pull request with your changes.
