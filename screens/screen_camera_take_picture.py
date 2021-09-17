import os
import cv2

#------------------------------------------------------------------------------

from kivy.metrics import dp
from kivy.clock import Clock
from kivy.graphics.texture import Texture  # @UnresolvedImport
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage

#------------------------------------------------------------------------------

from components import screen
from components.buttons import CloseButton, RoundedButton
from components.webfont import fa_icon

#------------------------------------------------------------------------------

class CameraTakePictureScreen(screen.AppScreen):

    def __init__(self, **kw):
        self.picture_taken_callback = kw.pop('picture_taken_callback', None)
        self.cancel_callback = kw.pop('cancel_callback', None)
        self.picture_filepath = kw.pop('picture_filepath', None)
        self.image_width = kw.pop('image_width', 640)
        self.image_height = kw.pop('image_height', 480)
        super(CameraTakePictureScreen, self).__init__(**kw)

        self.container = FloatLayout(
            size_hint=(None, None, ),
            pos_hint={'center_x':0.5, 'center_y': 0.5, },
            width=self.image_width,
            height=self.image_height, 
        )
        self.add_widget(self.container)

        self.camera_texture = Image(
            id='camera_texture',
            size_hint=(1, 1, ),
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={'center_x':0.5, 'center_y': 0.5, },
        )
        self.container.add_widget(self.camera_texture)

        btn1 = RoundedButton(
            id='take_picture_button',
            size_hint=(None, None, ),
            pos_hint={"center_x": 0.5, "y": 0.0, },
            width=dp(50),
            height=dp(50),
            text=fa_icon('camera'),
            on_release=self.on_capture,
        )
        self.container.add_widget(btn1)

        btn2 = CloseButton(
            id='cancel_button',
            pos_hint = {"right": 1, "top": 1, },
            text=fa_icon('window-close'),
            on_release = self.on_cancel_button_clicked,
        )
        self.container.add_widget(btn2)

        self.camera_capture = cv2.VideoCapture(int(os.environ.get('DEV_VIDEO_INDEX', '0')))  # @UndefinedVariable
        self.camera_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.image_width)  # @UndefinedVariable
        self.camera_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.image_height)  # @UndefinedVariable
        self.fps = self.camera_capture.get(cv2.CAP_PROP_FPS)  # @UndefinedVariable

        if self.fps == 0 or self.fps == 1:
            self.fps = 1.0 / 10
        elif self.fps > 1:
            self.fps = 1.0 / (self.fps / 2.0)

        self.camera_task = Clock.schedule_interval(self.on_camera_update, 1.0 / 20)

    def on_camera_update(self, dt):
        ret, frame = self.camera_capture.read()
        if not ret:
            return
        buf1 = cv2.flip(frame, 0)  # @UndefinedVariable
        buf = buf1.tostring()
        image_texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]),
            colorfmt='bgr',
        )
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.camera_texture.texture = image_texture

    def on_capture(self, *args):
        self.camera_task.cancel()
        self.camera_capture.release()
        if self.picture_filepath:
            CoreImage(self.camera_texture.texture).save(self.picture_filepath, flipped=True)
        if self.picture_taken_callback:
            self.picture_taken_callback(self.picture_filepath)

    def on_cancel_button_clicked(self, *args):
        self.camera_task.cancel()
        self.camera_capture.release()
        if self.cancel_callback:
            self.cancel_callback()
