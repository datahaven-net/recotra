import os
import cv2

#------------------------------------------------------------------------------

from kivy.lang import Builder
from kivy.uix.label import Label

#------------------------------------------------------------------------------

from components import screen

#------------------------------------------------------------------------------

MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

#------------------------------------------------------------------------------

class ScannedQRTextLabel(Label):

    def on_text(self, instance, value):
        if value:
            if self.parent.parent.scan_qr_callback:
                self.parent.parent.scan_qr_callback(value)


class CameraScanQRScreen(screen.AppScreen):

    def __init__(self, **kw):
        self.scan_qr_callback = kw.pop('scan_qr_callback', None)
        self.cancel_callback = kw.pop('cancel_callback', None)
        print('loading screen_camera_scan_qr.kv')
        Builder.load_file(os.path.join(MODULE_DIRECTORY, "screen_camera_scan_qr.kv"))
        super(CameraScanQRScreen, self).__init__(**kw)

    def on_enter(self, *args):
        print('on_enter', self.ids.zbarcam.xcamera.play, self.ids.zbarcam.xcamera._camera, self.ids.zbarcam.xcamera._camera._device)
        # if self.ids.zbarcam.xcamera._camera._device is None:
        #     self.ids.zbarcam.xcamera._camera.init_camera()
        # self.ids.zbarcam.start()
        return screen.AppScreen.on_enter(self, *args)

    def on_leave(self, *args):
        print('on_leave', self.ids.zbarcam.xcamera.play, self.ids.zbarcam.xcamera._camera, self.ids.zbarcam.xcamera._camera._device)
        # self.ids.zbarcam.xcamera.play = False
        # self.ids.zbarcam.xcamera._camera._device.release()
        # self.ids.zbarcam.xcamera._camera._device = None
        # cv2.destroyAllWindows()  # @UndefinedVariable
        self.ids.zbarcam.stop()
        return screen.AppScreen.on_leave(self, *args)

    def on_cancel_button_clicked(self, *args):
        if self.cancel_callback:
            self.cancel_callback()
