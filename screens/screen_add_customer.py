from kivy.app import App

#------------------------------------------------------------------------------

from components import screen
from components.webfont import fa_icon

from screens import screen_camera_take_picture

from storage import local_storage

#------------------------------------------------------------------------------

kv = """
<AddCustomerScreen>:
    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, 1
            pos_hint: {'top': 1}

            BoxLayout:
                orientation: 'vertical'
                pos_hint: {"top":1}
                size_hint_y: None
                height: self.minimum_height
                padding: 20
                spacing: 10

                Label:
                    text_size: self.size
                    height: 30
                    halign: "right"
                    text: "Photo:"

                Image:
                    id: customer_photo_picture_image
                    size_hint: None, None
                    pos_hint: {"right":1}
                    size: 200, 150
                    source: ''

                    canvas.before:
                        Color:
                            rgba: (0, 0, 0, 1)
                        Line:
                            rectangle: (self.x-2, self.y-2, self.width+4, self.height+4) 
                            width: 2

                    RoundedButton:
                        width: 30
                        height: 30
                        x: self.parent.x + self.parent.width - 40
                        y: self.parent.y + self.parent.height - 40
                        font_size: '24'
                        background_color: 0, 0, 0, 0
                        color: 0.9, 0.9, 0.9, 1
                        markup: True
                        text: fa_icon('camera')
                        on_release: root.on_customer_photo_button_clicked()

            BoxLayout:
                orientation: 'vertical'
                pos_hint: {'top': 1}
                size_hint_y: None
                height: self.minimum_height
                padding: 20
                spacing: 10

                Label:
                    text_size: self.size
                    valign: "bottom"
                    halign: "left"
                    text: "First name:"
                TextInput:
                    id: customer_first_name_input
                    text: ""
                    right: self.width
                    width: 250
                    height: 30
                    size_hint_x: None
                    size_hint_y: None

                Label:
                    text_size: self.size
                    valign: "bottom"
                    halign: "left"
                    text: "Last name:"
                TextInput:
                    id: customer_last_name_input
                    text: ""
                    width: 250
                    height: 30
                    size_hint_x: None
                    size_hint_y: None

                Label:
                    text_size: self.size
                    valign: "bottom"
                    halign: "left"
                    text: "Phone:"
                TextInput:
                    id: customer_phone_input
                    text: ""
                    width: 250
                    height: 30
                    size_hint_x: None
                    size_hint_y: None

                Label:
                    text_size: self.size
                    valign: "bottom"
                    halign: "left"
                    text: "E-mail:"
                TextInput:
                    id: customer_email_input
                    text: ""
                    width: 250
                    height: 30
                    size_hint_x: None
                    size_hint_y: None

                Label:
                    text_size: self.size
                    valign: "bottom"
                    halign: "left"
                    text: "Address:"
                TextInput:
                    id: customer_address_input
                    text: ""
                    width: 250
                    height: 90
                    size_hint_x: None
                    size_hint_y: None

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            padding: 10
            spacing: 2

            RoundedButton:
                text: "Save Customer"
                width: 120
                size_hint_x: None
                on_release: root.on_add_customer_save_button_clicked()
"""

class AddCustomerScreen(screen.AppScreen):

    new_customer_id = None

    def scr_manager(self):
        return App.get_running_app().root.ids.scr_manager

    def take_pic_screen(self):
        return self.scr_manager().get_screen('camera_take_picture_screen')

    def clean_input_fields(self):
        self.ids.customer_first_name_input.text = ''
        self.ids.customer_last_name_input.text = ''
        self.ids.customer_phone_input.text = ''
        self.ids.customer_email_input.text = ''
        self.ids.customer_address_input.text = ''
        self.ids.customer_photo_picture_image.source = ''

    def on_pre_enter(self, *args):
        if self.new_customer_id is None:
            self.new_customer_id = local_storage.create_new_customer_info()
            self.clean_input_fields()

    def on_customer_photo_button_clicked(self, *args):
        self.camera_screen = screen_camera_take_picture.CameraTakePictureScreen(
            name='camera_take_picture_screen',
            picture_taken_callback=self.on_customer_photo_picture_ready,
            picture_filepath=local_storage.customer_photo_filepath(self.new_customer_id), 
        )
        self.scr_manager().add_widget(self.camera_screen)
        self.scr_manager().current = 'camera_take_picture_screen'

    def on_customer_passport_button_clicked(self, *args):
        self.camera_screen = screen_camera_take_picture.CameraTakePictureScreen(
            name='camera_take_picture_screen',
            picture_taken_callback=self.on_customer_passport_picture_ready,
            picture_filepath=local_storage.customer_passport_filepath(self.new_customer_id),
        )
        self.scr_manager().add_widget(self.camera_screen)
        self.scr_manager().current = 'camera_take_picture_screen'

    def on_customer_photo_picture_ready(self, *args):
        self.ids.customer_photo_picture_image.source = args[0]
        self.scr_manager().current = 'add_customer_screen'
        self.scr_manager().remove_widget(self.camera_screen)

    def on_add_customer_save_button_clicked(self, *args):
        local_storage.write_customer_info(dict(
            customer_id=self.new_customer_id,
            first_name=self.ids.customer_first_name_input.text,
            last_name=self.ids.customer_last_name_input.text,
            phone=self.ids.customer_phone_input.text,
            email=self.ids.customer_email_input.text,
            address=self.ids.customer_address_input.text,
        ))
        self.scr_manager().get_screen('customers_screen').ids.customers_view.populate()
        self.scr_manager().current = 'customers_screen'
