from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.core.window import Window
from photo_manager import Manager
from kivymd.toast import toast

Window.minimum_height = 500
Window.minimum_width = 800


class MainApp(MDApp):
    theme_cls = ThemeManager()
    current_index = 0
    actions = dict()
    sorter: Manager

    def __init__(self):
        super().__init__()
        self.title = 'BTS Photo Sorter'
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self.root)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_start(self):
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.theme_style = 'Dark'
        self.sorter = Manager()
        self.__load_photos()

    def __load_photos(self):
        photo_list = self.sorter.photos
        if len(photo_list) > 0:
            self.root.ids.image.source = photo_list[self.current_index][1]
            self.current_index = 0
            self.root.ids.slider.min = 1
            self.root.ids.slider.max = len(photo_list)
        else:
            toast(text='Не удалось открыть целевой альбом. Проверьте конфигурационный файл.',
                  duration=10)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.action(keycode[1])

    def action(self, key):
        if len(self.sorter.photos) == 0:
            if key == 'r':
                toast(text='Сброс сортировки...')
                self.sorter.reset()
                self.__load_photos()
            return

        if key == 'right':
            self.advance()
            return
        if key == 'left':
            self.back()
            return

        current_id = self.sorter.photos[self.current_index][0]
        need_action = current_id not in self.actions or self.actions[current_id] is not key
        if key in self.sorter.keys_map and need_action:
            response = self.sorter.move(self.current_index, key)
            if response == 1:
                self.actions[current_id] = key
                toast('Фотография перемещена в альбом "' +\
                      self.sorter.keys_map[key] + '"')
                self.advance()
            else:
                toast('Ошибка при перемещении.' + str(response))

    def advance(self):
        if self.current_index < len(self.sorter.photos) - 1:
            self.current_index += 1
            self.display()
        else:
            toast(text='Достигнут конец альбома.')

    def back(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display()
        else:
            toast(text='Данная фотография является первой в альбоме.')

    def display(self):
        self.root.ids.slider.value = self.current_index + 1
        self.root.ids.image.source = self.sorter.photos[self.current_index][1]

    def set_index(self, instance, value):
        self.current_index = value - 1
        self.display()


if __name__ == '__main__':
    MainApp().run()

