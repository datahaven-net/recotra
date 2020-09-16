from kivy.app import App

#------------------------------------------------------------------------------

from components import screen
from components.webfont import fa_icon
# from components.fa_image import FaImage 

from screens import screen_camera_take_picture

from storage import local_storage

#------------------------------------------------------------------------------

kv = """
<AddCustomerScreen>:
    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint: 1, 1
            orientation: 'horizontal'
            BoxLayout:
                orientation: 'vertical'
                padding: 10
                spacing: 10
                Label:
                    text_size: self.size
                    height: 30
                    valign: "bottom"
                    halign: "right"
                    text: "Photo:"
                Image:
                    canvas.before:
                        Color:
                            rgba: (0, 0, 0, 1)
                        Line:
                            rectangle: (self.x, self.y, self.width, self.height) 
                            width: 2
                    id: customer_photo_picture_image
                    size_hint: None, None
                    pos_hint: {"right":1}
                    size: 200, 160
                    source: ''
                    Button:
                        width: 30
                        height: 30
                        x: self.parent.x + self.parent.width - 40
                        y: self.parent.y + self.parent.height - 40
                        font_size: '24'
                        background_color: 0, 0, 0, 0
                        color: 0.5, 0.5, 0.9, 1
                        text: fa_icon('camera')
                        on_release: root.on_customer_photo_button_clicked()

                Label:
                    text_size: self.size
                    height: 30
                    valign: "bottom"
                    halign: "right"
                    text: "Passport / ID:"

                Image:
                    canvas.before:
                        Color:
                            rgba: (0, 0, 0, 1)
                        Line:
                            rectangle: (self.x, self.y, self.width, self.height) 
                            width: 2
                    id: customer_passport_picture_image
                    pos_hint: {"right":1}
                    size_hint: None, None
                    size: 200, 180
                    source: ''
                    Button:
                        width: 30
                        height: 30
                        x: self.parent.x + self.parent.width - 40
                        y: self.parent.y + self.parent.height - 40
                        font_size: '24'
                        background_color: 0, 0, 0, 0
                        color: 0.5, 0.5, 0.9, 1
                        text: fa_icon('camera')
                        on_release: root.on_customer_passport_button_clicked()


            BoxLayout:
                orientation: 'vertical'
                padding: 10
                spacing: 10
                Label:
                    text_size: self.size
                    valign: "bottom"
                    halign: "left"
                    text: "First name:"
                TextInput:
                    id: customer_first_name_input
                    text: "John"
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
                    text: "Smith"
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
                    text: "+123456789"
                    width: 250
                    height: 30
                    size_hint_x: None
                    size_hint_y: None
                Label:
                    text_size: self.size
                    valign: "bottom"
                    halign: "left"
                    text: "email:"
                TextInput:
                    id: customer_email_input
                    text: "smith.john@gmail.com"
                    width: 250
                    height: 30
                    size_hint_x: None
                    size_hint_y: None

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            padding: 10
            spacing: 2
            RoundedButton:
                id: buy_save_customer_button
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

    def on_pre_enter(self, *args):
        if self.new_customer_id is None:
            self.new_customer_id = local_storage.create_new_customer_info()

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

    def on_customer_passport_picture_ready(self, *args):
        self.ids.customer_passport_picture_image.source = args[0]
        self.scr_manager().current = 'add_customer_screen'
        self.scr_manager().remove_widget(self.camera_screen)

    def on_add_customer_save_button_clicked(self, *args):
        local_storage.write_customer_info(dict(
            customer_id=self.new_customer_id,
            first_name=self.ids.customer_first_name_input.text,
            last_name=self.ids.customer_last_name_input.text,
        ))
        new_list = local_storage.make_customers_ui_data(
            customers_list=local_storage.load_customers_list(sort_by='customer_id'),
        )
        print(new_list)
        # App.get_running_app().root.ids.customers_list_view.data = new_list
