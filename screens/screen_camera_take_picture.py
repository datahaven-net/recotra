import time

#------------------------------------------------------------------------------

from components import screen

#------------------------------------------------------------------------------

kv = """
#:import XCamera kivy_garden.xcamera.XCamera

<CameraTakePictureScreen>:
    FloatLayout:
        orientation: 'vertical'
        XCamera:
            id: xcamera
            on_picture_taken: root.on_capture(*args)
        # BoxLayout:
        #     orientation: 'horizontal'
        #     size_hint: 1, None
        #     height: sp(50)
            # Button:
            #     text: 'Set landscape'
            #     on_release: xcamera.force_landscape()
            # Button:
            #     text: 'Restore orientation'
            #     on_release: xcamera.restore_orientation()
"""

class CameraTakePictureScreen(screen.AppScreen):

    def on_capture(self, *args):
#         camera = self.ids['camera']
#         timestr = time.strftime("%Y%m%d_%H%M%S")
#         camera.export_to_png("/tmp/IMG_{}.png".format(timestr))
        print("Captured", args)
