from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty  # @UnresolvedImport

#------------------------------------------------------------------------------

_Debug = False

#------------------------------------------------------------------------------

class AppScreen(Screen):

    title = StringProperty('')

    def __init__(self, **kw):
        super(AppScreen, self).__init__(**kw)

    def get_title(self):
        return self.title

    def app(self):
        return App.get_running_app()

    def main_win(self):
        return self.app().main_window

    def scr_manager(self):
        return self.main_win().ids.scr_manager

    def scr(self, screen_name):
        return self.scr_manager().get_screen(screen_name)
