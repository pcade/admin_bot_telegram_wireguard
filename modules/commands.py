import subprocess
import json
from telebot.types import InputFile
from modules.states import COMMAND_GEN_CONFIG

def handle_create_request(bot, chat_id, user_data):
    if chat_id in user_data:
        # Выполняем команды на backend
        try:
            command = COMMAND_GEN_CONFIG
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            stdout, stderr = process.communicate()
            output_dict = json.loads(stdout)
            path_conf = output_dict['conf']
            path_qr = output_dict['qr']

            bot.send_message(chat_id, f"Конфигурация успешно создана!\n{path_conf}\n{ path_qr}")

            with open(path_qr, "rb") as photo:
                bot.send_photo(chat_id, photo=InputFile(photo))

            with open(path_conf, "rb") as file:
                bot.send_document(
                    chat_id,
                    document=InputFile(file),
                    visible_file_name= path_conf.split('/')[-1],
                    caption="Ваш конфигурационный файл"
                )

        except subprocess.CalledProcessError as e:
            bot.send_message(chat_id, f"Ошибка при выполнении команды:\n{e.stderr}", reply_markup=menu)
    else:
        bot.send_message(chat_id, "Сначала введите данные для конфигурации.", reply_markup=menu)