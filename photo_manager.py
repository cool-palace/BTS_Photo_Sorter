import vk_api
from config import *


class Manager:
    def __init__(self):
        self.vk = Manager.__vk_connect()
        self.album_map = self.__target_albums()
        self.photos = self.__photos()

    @staticmethod
    def __captcha_handler(captcha):
        key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
        return captcha.try_again(key)

    @staticmethod
    def __vk_connect():
        vk_session = vk_api.VkApi(LOGIN, PASSWORD,
                                  app_id=APP_ID,
                                  scope=PERMISSIONS,
                                  config_filename='vk_config.v2.json',
                                  captcha_handler=Manager.__captcha_handler)
        try:
            vk_session.auth()
        except vk_api.exceptions.AuthError as error:
            print(error)
        vk = vk_session.get_api()
        return vk

    def __reset(self):
        for name in self.album_map:
            response = self.vk.photos.get(owner_id=self.__user_id(),
                                          album_id=self.album_map[name])
            for item in response['items']:
                self.vk.photos.move(owner_id=self.__user_id(),
                                    target_album_id=self.__valid_target_album_id(),
                                    photo_id=item['id'])

    def __user_id(self) -> str:
        return str(self.vk.users.get()[0]['id'])

    def __target_albums(self) -> dict():
        response = self.vk.photos.getAlbums(owner_id=self.__user_id())
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

    def __valid_source_album_id(self) -> str:
        response = self.vk.photos.getAlbums(owner_id=self.__user_id())
        for item in response['items']:
            if item['id'] == int(ALBUM_ID):
                return ALBUM_ID
            if item['title'] == ALBUM_ID:
                return str(item['id'])
        return ''

    @staticmethod
    def link(item) -> str:
        for size in item['sizes']:
            if size['type'] == 'z':
                return size['url']
        for size in item['sizes']:
            if size['type'] == 'y':
                return size['url']
        return item['sizes'][-1]['url']

    def __photos(self) -> []:
        valid_id = self.__valid_source_album_id()
        result = []
        if len(valid_id) == 0:
            return result
        response = self.vk.photos.get(owner_id=self.__user_id(),
                                      album_id=valid_id)
        for item in response['items']:
            photo_id = item['id']
            url = Manager.link(item)
            result.append((photo_id, url))
        return result
