import cv2

from collections import namedtuple
import PIL
from pyzbar import pyzbar

#------------------------------------------------------------------------------

from kivy.properties import ListProperty  # @UnresolvedImport
from kivy.clock import Clock
from kivy.graphics.texture import Texture  # @UnresolvedImport
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

#------------------------------------------------------------------------------

from components import screen
from components.buttons import RoundedButton

#------------------------------------------------------------------------------

BarSymbol = namedtuple('BarSymbol', ['type', 'data'])

#------------------------------------------------------------------------------

class CameraScanQRScreen(screen.AppScreen):

    symbols = ListProperty([])
    code_types = ListProperty(set(pyzbar.ZBarSymbol))

    def __init__(self, **kw):
        self.scan_qr_callback = kw.pop('scan_qr_callback', None)
        self.cancel_callback = kw.pop('cancel_callback', None)
        super(CameraScanQRScreen, self).__init__(**kw)

        f_layout = FloatLayout()
        self.add_widget(f_layout)

        img = Image(id='camera_texture')
        img.size_hint = (1, 1, )
        img.allow_stretch = True
        img.keep_ratio = True
        img.pos_hint = {'center_x':0.5, 'top': 1.0, }
        f_layout.add_widget(img)
        self.camera_texture = img

        btn = RoundedButton(id='cancel_button', text=' cancel ')
        btn.pos_hint = {"x":0.0, "y": 0.0, }
        btn.size_hint = (None, None, )
        btn.width = 50
        btn.height = 50
        btn.on_release = self.on_cancel_button_clicked
        f_layout.add_widget(btn)

        self.camera_capture = cv2.VideoCapture(0)  # @UndefinedVariable
        self.camera_task = Clock.schedule_interval(self.on_camera_update, 1.0 / 20)

    def on_cancel_button_clicked(self, *args):
        self.camera_task.cancel()
        self.camera_capture.release()
        if self.cancel_callback:
            self.cancel_callback()

    def on_camera_update(self, dt):
        ret, frame = self.camera_capture.read()
        if ret:
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
            for code in codes:
                symbol = BarSymbol(type=code.type, data=code.data)
                self.symbols.append(symbol)
            if self.symbols:
                self.camera_task.cancel()
                self.camera_capture.release()
                if self.scan_qr_callback:
                    self.scan_qr_callback(', '.join([symbol.data.decode('utf-8') for symbol in self.symbols]))
