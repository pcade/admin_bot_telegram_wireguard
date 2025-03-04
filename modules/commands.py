import subprocess
import json
from telebot.types import InputFile
from utils.utils import COMMAND_GEN_CONFIG

def generate_configuration():
    """
    Генерирует конфигурацию WireGuard и возвращает пути к файлам.
    """
    try:
        command = COMMAND_GEN_CONFIG  # Замените на реальную команду
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise Exception(f"Ошибка при выполнении команды: {stderr}")

        output_dict = json.loads(stdout)
        return output_dict['conf'], output_dict['qr']
    except Exception as e:
        raise Exception(f"Ошибка при генерации конфигурации: {e}")

def send_configuration_files(bot, chat_id, config_path, qr_path):
    """
    Отправляет конфигурационные файлы пользователю.
    """
    try:
        with open(qr_path, "rb") as qr_file:
            bot.send_photo(chat_id, photo=InputFile(qr_file))

        with open(config_path, "rb") as config_file:
            bot.send_document(
                chat_id,
                document=InputFile(config_file),
                visible_file_name=config_path.split('/')[-1],
                caption="Ваш конфигурационный файл"
            )
    except Exception as e:
        raise Exception(f"Ошибка при отправке файлов: {e}")