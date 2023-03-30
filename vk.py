import requests
from pprint import pprint


class Vk:
    url = 'https://api.vk.com/method/'

    def __init__(self, token):
        self.params = {
            'access_token': token,
            'v': '5.131'}

    def user(self):
        user_url = self.url + 'users.get'
        user_params = {'user_ids': '1'}
        res = requests.get(user_url, params={**self.params, **user_params})
        pprint(res.json())

    def id(self, user_id):
        try:
            int(user_id)
            result = user_id
        except ValueError:
            url = self.url + 'utils.resolveScreenName'
            id_params = {'screen_name': user_id}
            res = requests.get(url, params={**self.params, **id_params}).json()
            result = res['response']['object_id']
        return result

    def get_photos(self, user_id, count):
        photos_url = self.url + 'photos.get'
        user_id = self.id(user_id=user_id)
        print(f'Найден id: {user_id}')
        photos_params = {'owner_id': user_id,
                         'album_id': 'profile',
                         'extended': 1,
                         'count': count,
                         'rev': 1}
        res = requests.get(photos_url, params={**self.params, **photos_params}).json()
        photos_full = res['response']['items']
        print('Получен доступ к фотографиям')
        photos = []
        for i in photos_full:
            likes = i['likes']['count']
            has_max = False
            max_res_ind = 0
            for m, val in enumerate(i['sizes']):
                if val['type'] == 'w':
                    has_max = True
                    max_res_ind = m
                    break
            if has_max:
                letter = 'w'
                url = i['sizes'][max_res_ind]['url']
            else:
                letter = i['sizes'][-1]['type']
                url = i['sizes'][-1]['url']
            photos.append({'date': i['date'], 'likes': likes, 'type': letter, 'url': url})
        print('Отобраны аватары наилучшего качества')

        return photos
