import cv2

#------------------------------------------------------------------------------

from kivy.clock import Clock
from kivy.graphics.texture import Texture  # @UnresolvedImport
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.button import Button

#------------------------------------------------------------------------------

from components import screen

#------------------------------------------------------------------------------

class CameraTakePictureScreen(screen.AppScreen):

    def __init__(self, **kw):
        self.picture_taken_callback = kw.pop('picture_taken_callback', None)
        self.picture_filepath = kw.pop('picture_filepath', None)
        super(CameraTakePictureScreen, self).__init__(**kw)
        
        f_layout = FloatLayout()
        self.add_widget(f_layout)

        img = Image(id='camera_texture')
        img.size_hint = (1, 1, )
        img.allow_stretch = True
        img.keep_ratio = True
        img.pos_hint = {'center_x':0.5, 'top': 1.0, }
        f_layout.add_widget(img)
        self.camera_texture = img

        btn = Button(id='take_picture_button', text='click')
        btn.pos_hint = {"x":0.0, "y": 0.0, }
        btn.size_hint = (None, None, )
        btn.width = 50
        btn.height = 50
        btn.on_release = self.on_capture
        f_layout.add_widget(btn)

        self.camera_capture = cv2.VideoCapture(0)  # @UndefinedVariable
        self.camera_task = Clock.schedule_interval(self.on_camera_update, 1.0 / 20)

    def on_camera_update(self, dt):
        ret, frame = self.camera_capture.read()
        if ret:
            buf1 = cv2.flip(frame, 0)  # @UndefinedVariable
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.camera_texture.texture = image_texture

    def on_capture(self):
        self.camera_task.cancel()
        self.camera_capture.release()
        if self.picture_filepath:
            CoreImage(self.camera_texture.texture).save(self.picture_filepath, flipped=True)
        if self.picture_taken_callback:
            self.picture_taken_callback(self.picture_filepath)
