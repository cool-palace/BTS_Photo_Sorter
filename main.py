from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.core.window import Window
from photo_manager import Manager
from kivymd.toast import toast


class MainApp(MDApp):
    theme_cls = ThemeManager()
    sorter = Manager()
    current_index = 0
    photo_list = []
    actions = dict()

    def __init__(self):
        super().__init__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self.root)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_start(self):
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.theme_style = 'Dark'
        self.__load_photos()

    def __load_photos(self):
        photo_list = self.sorter.photos
        if len(photo_list) > 0:
            self.root.ids.image.source = photo_list[self.current_index][1]
            self.current_index = 0
        else:
            toast(text='Не удалось открыть целевой альбом. Проверьте конфигурационный файл.',
                  duration=10)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.action(keycode[1])

    def action(self, key):
        if key in self.sorter.keys_map:
            response = self.sorter.move(self.current_index, key)
            if response == 1:
                toast('Фотография перемещена.')
                self.advance()
            else:
                toast('Ошибка при перемещении.' + str(response))
        elif len(self.sorter.photos) == 0 and key == 'r':
            self.sorter.reset()
            self.__load_photos()

    def move(self, keycode):
        self.keys_map[keycode[1]]

    def advance(self):
        if self.current_index < len(self.sorter.photos) - 1:
            self.current_index += 1
            self.root.ids.image.source = self.sorter.photos[self.current_index][1]

    def back(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.root.ids.image.source = self.sorter.photos[self.current_index][1]


if __name__ == '__main__':
    MainApp().run()

