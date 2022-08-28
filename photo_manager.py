import vk_api
from config import *


class Manager:
    def __init__(self):
        self.vk = Manager.__vk_connect()

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

    # def user_id(self):
    #     return vk.users.get()[]
