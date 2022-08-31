from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput


class Handler:
    @staticmethod
    def check_captcha(text, captcha, popup):
        captcha.try_again(text)
        popup.dismiss()

    @staticmethod
    def captcha_handler(captcha):
        content = BoxLayout(orientation='vertical')
        popup = Popup(title='Введите капчу:',
                      size_hint=[.5, .5],
                      content=content,
                      auto_dismiss=False)
        popup.content.add_widget(AsyncImage(source=captcha.get_url()))
        input_field = TextInput(multiline=False,
                                on_text_validate=lambda *args, captcha_=captcha, popup_=popup:
                                Handler.check_captcha((args[0].text.strip()), captcha_, popup_),
                                size_hint_y=.2)
        popup.content.add_widget(input_field)
        popup.open()
