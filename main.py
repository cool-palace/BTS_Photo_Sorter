from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.core.window import Window
from kivymd.toast import toast


class MainApp(MDApp):
    theme_cls = ThemeManager()

    def __init__(self):
        super().__init__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self.root)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.pressed_actions = {
            '1': 'RM',
            '2': 'Suga',
            '3': 'J-Hope',
            '4': 'Jin',
            '5': 'V',
            '6': 'Jimin',
            '7': 'Jungkook'
        }

    def on_start(self):
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.theme_style = 'Dark'

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The keys', keycode, 'have been pressed down')
        print('You pressed the key', keycode[1], '.', sep=' ', end='\n')
        print(self.pressed_actions[keycode[1]])


if __name__ == '__main__':
    MainApp().run()

