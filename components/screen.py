from kivy.uix.screenmanager import Screen

#------------------------------------------------------------------------------

class AppScreen(Screen):

    def get_title(self):
        return self.name
