from yandex import YandexDisk
from vk import Vk
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv


def backup():
    name = input('Введите id или nickname')
    count = input('Сколько фото хотите сохранить?')
    folder = input('В какую папку хотите сохранить фотографии?')
    photo_dict = vk.get_photos(name, count)
    log_dict = ya.upload_photo(photo_dict, folder)
    with open('freddy.json', 'w') as f:
        json.dump(log_dict, f)
    return f'Фото с аккаунта {name} успешно скопированы на YandexDisk'


if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), 'tokens.env')
    load_dotenv(dotenv_path)
    VKTOKEN = os.environ.get("VKTOKEN")
    TOKEN = os.environ.get("TOKEN")
    vk = Vk(token=VKTOKEN)
    ya = YandexDisk(token=TOKEN)

    print(backup())

