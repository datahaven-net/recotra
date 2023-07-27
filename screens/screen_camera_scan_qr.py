import os
import cv2

from collections import namedtuple
import PIL
from pyzbar import pyzbar

#------------------------------------------------------------------------------

from kivy.properties import ListProperty  # @UnresolvedImport
from kivy.clock import Clock
from kivy.graphics.texture import Texture  # @UnresolvedImport
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout

#------------------------------------------------------------------------------

from components import screen
from components.buttons import CloseButton
from components.webfont import fa_icon

#------------------------------------------------------------------------------

_Debug = False

#------------------------------------------------------------------------------

BarSymbol = namedtuple('BarSymbol', ['type', 'data'])

#------------------------------------------------------------------------------

class CameraScanQRScreen(screen.AppScreen):

    symbols = ListProperty([])
    code_types = ListProperty(set(pyzbar.ZBarSymbol))

    def __init__(self, **kw):
        self.scan_qr_callback = kw.pop('scan_qr_callback', None)
        self.cancel_callback = kw.pop('cancel_callback', None)
        self.image_width = kw.pop('image_width', 640)
        self.image_height = kw.pop('image_height', 480)
        super(CameraScanQRScreen, self).__init__(**kw)

        self.container = FloatLayout(
            size_hint=(None, None, ),
            pos_hint={'center_x':0.5, 'center_y': 0.5, },
            width=self.image_width,
            height=self.image_height, 
        )
        self.add_widget(self.container)

        self.camera_texture = Image(
            # id='camera_texture',
            size_hint=(1, 1, ),
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={'center_x':0.5, 'center_y': 0.5, },
        )
        self.container.add_widget(self.camera_texture)

        btn = CloseButton(
            # id='cancel_button',
            pos_hint = {"right": 1, "top": 1, },
            text=fa_icon('window-close'),
            on_release = self.on_cancel_button_clicked,
        )
        self.container.add_widget(btn)

        self.camera_capture = cv2.VideoCapture(int(os.environ.get('RECOTRA_CAMERA_INDEX', '0')))  # @UndefinedVariable
        self.camera_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.image_width)  # @UndefinedVariable
        self.camera_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.image_height)  # @UndefinedVariable
        self.fps = self.camera_capture.get(cv2.CAP_PROP_FPS)  # @UndefinedVariable

        if self.fps == 0 or self.fps == 1:
            self.fps = 1.0 / 10
        elif self.fps > 1:
            self.fps = 1.0 / (self.fps / 2.0)

        self.camera_task = Clock.schedule_interval(self.on_camera_update, self.fps)

    def on_camera_update(self, dt):
        ret, frame = self.camera_capture.read()
        if not ret:
            return
        buf1 = cv2.flip(frame, 0)  # @UndefinedVariable
        buf = buf1.tostring()
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.camera_texture.texture = image_texture
        image_data = self.camera_texture.texture.pixels
        size = self.camera_texture.texture.size
        pil_image = PIL.Image.frombytes(mode='RGBA', size=size, data=image_data)
        self.symbols = []
        codes = pyzbar.decode(pil_image, symbols=self.code_types)
        if _Debug:
            print(1/self.fps, size, len(image_data), len(buf), len(codes))
        for code in codes:
            symbol = BarSymbol(type=code.type, data=code.data)
            self.symbols.append(symbol)
        if not self.symbols:
            return
        result_text = ', '.join([symbol.data.decode('utf-8') for symbol in self.symbols])
        if _Debug:
            print('scanned text:', result_text)
        self.camera_task.cancel()
        self.camera_capture.release()
        if self.scan_qr_callback:
            self.scan_qr_callback(result_text)

    def on_cancel_button_clicked(self, *args):
        self.camera_task.cancel()
        self.camera_capture.release()
        if self.cancel_callback:
            self.cancel_callback()
