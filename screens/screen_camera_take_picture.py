import os

#------------------------------------------------------------------------------

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy_garden.xcamera import XCamera

#------------------------------------------------------------------------------

from components import screen
from storage import local_storage

#------------------------------------------------------------------------------

class MyCamera(XCamera):

    def __init__(self, **kw):
        self.directory = local_storage.temp_dir()
        self.picture_filepath = kw.pop('picture_filepath', '')
        super(MyCamera, self).__init__(**kw)

    def on_picture_taken(self, *args):
        if self.picture_filepath:
            os.rename(args[0], self.picture_filepath)
        if self.parent.parent.return_screen:
            scr_manager = App.get_running_app().root.ids.scr_manager
            scr_manager.current = self.parent.parent.return_screen
            scr_manager.remove_widget(self.parent.parent)
            if self.picture_filepath:
                scr_manager.get_screen(self.parent.parent.return_screen).on_picture_taken(self.picture_filepath)


class CameraTakePictureScreen(screen.AppScreen):

    def __init__(self, **kw):
        self.return_screen = kw.pop('return_screen', '')
        picture_filepath = kw.pop('picture_filepath', '')
        super(CameraTakePictureScreen, self).__init__(**kw)
        f_layout = FloatLayout()
        self.add_widget(f_layout)
        my_camera = MyCamera(picture_filepath=picture_filepath)
        f_layout.add_widget(my_camera)        
