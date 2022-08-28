from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivymd.toast import toast


class MainApp(MDApp):
    theme_cls = ThemeManager()

    def on_start(self):
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.theme_style = 'Dark'


if __name__ == '__main__':
    MainApp().run()

