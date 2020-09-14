from kivy.app import App
from kivy.uix.camera import Camera

#------------------------------------------------------------------------------

from components import screen

#------------------------------------------------------------------------------

kv = """
<AddCustomerScreen>:
    BoxLayout:
        orientation: 'vertical'
        GridLayout:
            cols: 2
            padding: 10
            spacing: 10
            Label:
                text: "First name:"
            TextInput:
                id: customer_first_name_input
                text: "John"
                width: 250
                height: 30
                size_hint_x: None
                size_hint_y: None
            Label:
                text: "Last name:"
            TextInput:
                id: customer_last_name_input
                text: "Smith"
                width: 250
                height: 30
                size_hint_x: None
                size_hint_y: None
            Label:
                text: "Photo:"
            Button:
                id: customer_photo_button
                text: fa_icon('camera')
                height: 150
                width: 150
                size_hint_x: None
                size_hint_y: None
                on_release: root.on_customer_photo_button_clicked()
            Label:
                text: "Passport / ID:"
            Button:
                id: customer_passport_photo_button
                text: fa_icon('camera')
                height: 150
                width: 150
                size_hint_x: None
                size_hint_y: None
                on_release: root.on_customer_passport_button_clicked()
        BoxLayout:
            orientation: 'horizontal'
            padding: 10
            spacing: 2
            Button:
                id: buy_save_customer_button
                text: "Save Customer"
                width: 120
                size_hint_x: None
                on_release: root.on_add_customer_save_button_clicked()
"""

class AddCustomerScreen(screen.AppScreen):

    def on_customer_photo_button_clicked(self):
#         camera_object = Camera(play=False)
#         camera_object.play = True
#         camera_object.resolution = (300, 300, )
#         camera_object.export_to_png('/tmp/selfie.png')
        App.get_running_app().root.ids.scr_manager.current = 'camera_take_picture_screen'

