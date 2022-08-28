import vk_api
from config import *


class Manager:
    def __init__(self):
        self.vk = Manager.__vk_connect()
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

    def __user_id(self) -> str:
        return str(self.vk.users.get()[0]['id'])

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
        result = []
        response = self.vk.photos.get(owner_id=self.__user_id(),
                                      album_id=ALBUM_ID)
        for item in response['items']:
            photo_id = item['id']
            url = Manager.link(item)
            result.append((photo_id, url))
        return result
