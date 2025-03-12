import subprocess
import json
from telebot.types import InputFile
from telebot import TeleBot
from utils.utils import COMMAND_GEN_CONFIG
from typing import Tuple

def generate_configuration(usr_name: str, usr_ip: str, usr_comment: str, usr_date: str) -> Tuple[str, str]:
    """
    Генерирует конфигурацию WireGuard и возвращает пути к файлам.

    :param usr_name: Имя пользователя (str);
    :param usr_ip: IP-адрес пользователя (str);
    :param usr_comment: Комментарий к конфигурации (str);
    :param usr_date: Дата окончания подписки (str);
    :return: tuple[str, str]: Пути к конфигурационным файлам.
    """
    try:
        command = f"{COMMAND_GEN_CONFIG} --json --name '{usr_name}' --ip '{usr_ip}' --comment '{usr_comment}' --date '{usr_date}'"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise Exception(f"Ошибка при выполнении команды: {stderr}")

        output_dict = json.loads(stdout)
        return output_dict['conf'], output_dict['qr']
    except Exception as e:
        raise Exception(f"Ошибка при генерации конфигурации: {e}")

def send_configuration_files(bot: TeleBot, chat_id: int, config_path: str, qr_path: str) -> None:
    """
    Отправляет конфигурационные файлы пользователю.

    :param bot: Объект бота (object.TeleBot);
    :param chat_id: ID чата (int);
    :param config_path: Путь к конфигурационному файлу (str);
    :param qr_path: Путь к файлу QR-кода (str);
    :return: None.
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

def show_config_ips() -> list:
    """
    Генерирует конфигурацию WireGuard и возвращает пути к файлам.

    :return: Список зарезервированных ip адресов (list).
    """
    try:
        command = f"{COMMAND_GEN_CONFIG} --config"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise Exception(f"Ошибка при выполнении команды: {stderr}")

#        print(stdout)  # Добавьте этот отладочный вывод
        return stdout
    except Exception as e:
        raise Exception(f"Ошибка при генерации конфигурации: {e}")

def daemon_reload() -> None:
    """
    Перезапускает демоны.

    :return: None.
    """
    try:
        command = f"{COMMAND_GEN_CONFIG} --daemonreload"
        subprocess.run(command, shell=True, check=True)

    except subprocess.CalledProcessError as e:
        raise Exception(f"Ошибка при генерации конфигурации: {e}")
    except Exception as e:
        raise Exception(f"Общая ошибка: {e}")

def remove_configuration(usr_ip: str) -> None:
    """
    Удаляем конфигурацию из WireGuard по ip.

    :param usr_ip: IP-адрес пользователя (str);
    :return: None.
    """
    try:
        command = f"{COMMAND_GEN_CONFIG} --remove '{usr_ip}'"
        subprocess.run(command, shell=True, check=True)

    except subprocess.CalledProcessError as e:
        raise Exception(f"Ошибка при удалении конфигурации: {e}")
    except Exception as e:
        raise Exception(f"Общая ошибка: {e}")

def remove_configuration_files(usr_name: str) -> None:
    """
    Удаляем конфигурацию из WireGuard по ip.

    :param usr_name: Имя пользователя (str);
    :return: None.
    """
    try:
        command = f"{COMMAND_GEN_CONFIG} --removeconfig '{usr_name}'"
        subprocess.run(command, shell=True, check=True)

    except subprocess.CalledProcessError as e:
        raise Exception(f"Ошибка при удалении конфигурации: {e}")
    except Exception as e:
        raise Exception(f"Общая ошибка: {e}")