import requests
from collections import Counter


class YandexDisk:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_link(self, file_path):
        up_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': file_path, 'overwrite': 'true'}
        response = requests.get(up_url, headers=headers, params=params)
        data = response.json()
        href = data.get('href')
        return href

    def upload_file(self, file_path, name):
        href = self._get_link(file_path=file_path)
        response = requests.put(href, data=open(name, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Файл залит')

    def create_folder(self, folder_name):
        print(f'Создание папки {folder_name}')
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        head = self.get_headers()
        params = {'path': folder_name}
        response = requests.get(url, params=params, headers=head)
        if response.status_code == 200:
            print('Такая папка уже есть')
        else:
            response = requests.put(url, params=params, headers=head)
            response.raise_for_status()
            if response.status_code == 201:
                print('Папка создана')
        return folder_name

    def upload_with_folder(self, file, text, folder_name):
        folder = self.create_folder(folder_name=folder_name)
        path = f'{folder}/{file}'
        href = self._get_link(file_path=path)
        response = requests.put(href, data=open(text, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Файл залит')

    def upload_photo(self, photos, folder_name):
        folder = self.create_folder(folder_name=folder_name)
        like_list = []
        log_dict = []
        for photo in photos:
            url = photo['url']
            date = photo['date']
            likes = photo['likes']
            name = f'{likes}likes.jpg'
            like_list.append(likes)
            counter = Counter(like_list)
            for v in counter.values():
                if v > 1:
                    name = f'{likes}likes{date}.jpg'
            log_dict.append({'file_name': name, 'size': photo['type']})
            path = f'{folder}/{name}'
            href = self._get_link(file_path=path)
            response = requests.get(url)
            data = response.content
            resp = requests.put(href, data=data)
            if resp.status_code == 201:
                print(f'Фото {name} загружено')
        return log_dict
