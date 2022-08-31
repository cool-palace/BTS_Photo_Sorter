import vk_api
from captcha_handler import Handler
from kivy.uix.popup import Popup
import json


class Manager:
    def __init__(self):
        config = Manager.__config()
        self.vk = Manager.__vk_connect(config)
        self.user_id = self.__user_id()
        self.source_album_id = self.__valid_source_album_id(config['album_id'])
        self.album_map = self.__target_albums()
        self.photos = self.__photos()
        self.keys_map = {
            '1': 'RM',
            '2': 'Suga',
            '3': 'J-Hope',
            '4': 'Jin',
            '5': 'V (Kim Taehyung)',
            '6': 'Jimin',
            '7': 'Jungkook'
        }

    @staticmethod
    def __config():
        file = open('config.json', 'r', encoding='utf-8')
        config = json.loads(file.read())
        file.close()
        return config

    @staticmethod
    def __vk_connect(config):
        vk_session = vk_api.VkApi(config['login'], config['password'],
                                  app_id=config['app_id'],
                                  scope=config['permissions'],
                                  config_filename='vk_config.v2.json',
                                  captcha_handler=Handler.captcha_handler)
        try:
            vk_session.auth()
        except vk_api.exceptions.AuthError as error:
            Popup(title=str(error),
                  size_hint=[.5, .5],
                  auto_dismiss=True).show()
        vk = vk_session.get_api()
        return vk

    def reset(self):
        for name in self.album_map:
            response = self.vk.photos.get(owner_id=self.user_id,
                                          album_id=self.album_map[name])
            for item in response['items']:
                self.vk.photos.move(owner_id=self.user_id,
                                    target_album_id=self.source_album_id,
                                    photo_id=item['id'])
        self.photos = self.__photos()

    def __user_id(self) -> str:
        return str(self.vk.users.get()[0]['id'])

    def __target_albums(self) -> dict():
        response = self.vk.photos.getAlbums(owner_id=self.user_id)
        names = {'RM', 'Suga', 'J-Hope', 'Jin', 'V (Kim Taehyung)', 'Jimin', 'Jungkook'}
        album_map = dict()
        for item in response['items']:
            if item['title'] in names:
                album_map[item['title']] = item['id']
        if len(album_map) == len(names):
            return album_map
        else:
            for name in names:
                if name not in album_map:
                    album_map[name] = self.vk.photos.createAlbum(title=name)['id']
        return album_map

    def __valid_source_album_id(self, album_id: str) -> str:
        response = self.vk.photos.getAlbums(owner_id=self.user_id)
        for item in response['items']:
            if item['id'] == int(album_id):
                return album_id
            if item['title'] == album_id:
                return str(item['id'])
        return ''

    @staticmethod
    def __link(item) -> str:
        link_y = ''
        for size in item['sizes']:
            if size['type'] == 'z':
                return size['url']
            elif size['type'] == 'y':
                link_y += size['url']
        if len(link_y) > 0:
            return link_y
        return item['sizes'][-1]['url']

    def __photos(self) -> []:
        valid_id = self.source_album_id
        result = []
        if len(valid_id) == 0:
            return result
        response = self.vk.photos.get(owner_id=self.user_id,
                                      album_id=valid_id,
                                      count=500)
        for item in response['items']:
            photo_id = item['id']
            url = Manager.__link(item)
            result.append((photo_id, url))
        return result

    def move(self, index: int, key: str):
        return self.vk.photos.move(owner_id=self.user_id,
                                   target_album_id=self.album_map[self.keys_map[key]],
                                   photo_id=self.photos[index][0])
