from kivy.app import App
from kivy.uix.camera import Camera

#------------------------------------------------------------------------------

from components import screen

from screens import screen_camera_take_picture

from storage import local_storage

#------------------------------------------------------------------------------

kv = """
<AddCustomerScreen>:
    
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'

            GridLayout:
                cols: 1
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

            GridLayout:
                cols: 1
                padding: 10
                spacing: 10
                Label:
                    text: "Photo:"
                BoxLayout:
                    orientation: 'horizontal'
                    Image:
                        canvas.before:
                            Color:
                                rgba: (0, 0, 0, 1)
                            Line:
                                points: [ \
                                    (self.pos[0]-1, self.pos[1]-1), \
                                    (self.pos[0]+self.size[0]+2, self.pos[1]-1), \
                                    (self.pos[0]+self.size[0]+2, self.pos[1]+self.size[1]+2), \
                                    (self.pos[0]-1, self.pos[1]+self.size[1]+2), \
                                ]
                                width: 1
                        id: customer_photo_picture_image
                        size_hint: None, None
                        size: 100, 100
                    Button:
                        id: customer_photo_button
                        text: fa_icon('camera')
                        height: 30
                        width: 30
                        size_hint_x: None
                        size_hint_y: None
                        on_release: root.on_customer_photo_button_clicked()                    
                Label:
                    text: "Passport / ID:"
                BoxLayout:
                    orientation: 'horizontal'
                    Image:
                        canvas.before:
                            Color:
                                rgba: (0, 0, 0, 1)
                            Line:
                                points: [ \
                                    (self.pos[0], self.pos[1]), \
                                    (self.pos[0]+self.size[0], self.pos[1]), \
                                    (self.pos[0]+self.size[0], self.pos[1]+self.size[1]), \
                                    (self.pos[0], self.pos[1]+self.size[1]), \
                                    (self.pos[0], self.pos[1]), \
                                ]
                                width: 2
                        id: customer_passport_picture_image
                        size_hint: None, None
                        size: 100, 100
                    Button:
                        id: customer_passport_photo_button
                        text: fa_icon('camera')
                        height: 30
                        width: 30
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

    new_customer_id = None

    def on_pre_enter(self, *args):
        if self.new_customer_id is None:
            self.new_customer_id = local_storage.create_new_customer_info()

    def on_customer_photo_button_clicked(self):
        take_pic_screen = screen_camera_take_picture.CameraTakePictureScreen(
            name='camera_take_picture_screen',
            return_screen='add_customer_screen',
            picture_filepath=local_storage.customer_photo_filepath(self.new_customer_id), 
        )
        App.get_running_app().root.ids.scr_manager.add_widget(take_pic_screen)
        App.get_running_app().root.ids.scr_manager.current = 'camera_take_picture_screen'

    def on_picture_taken(self, picture_filepath):
        print('123', picture_filepath, self.ids.customer_photo_picture_image)
        self.ids.customer_photo_picture_image.source = picture_filepath
