import os

#------------------------------------------------------------------------------

from kivy.app import App
from kivy.cache import Cache

#------------------------------------------------------------------------------

from components import screen
from components.webfont import fa_icon

from lib import render_pdf
from lib import system

from storage import local_storage

from screens import screen_camera_take_picture
from screens.screen_camera_scan_qr import CameraScanQRScreen

#------------------------------------------------------------------------------

_Debug = True

#------------------------------------------------------------------------------

kv = """
<EditCustomerScreen>:

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, 1
            pos_hint: {'top': 1}

            BoxLayout:
                orientation: 'vertical'
                pos_hint: {'top': 1}
                size_hint_y: None
                height: self.minimum_height
                padding: dp(20)
                spacing: dp(10)

                Label:
                    text_size: self.size
                    height: dp(30)
                    halign: "right"
                    text: "Photo:"

                Image:
                    id: customer_photo_picture_image
                    size_hint: None, None
                    pos_hint: {'right':1}
                    size: 200, 150
                    source: ''

                    canvas.before:
                        Color:
                            rgba: (0, 0, 0, 1)
                        Line:
                            rectangle: (self.x-2, self.y-2, self.width+4, self.height+4) 
                            width: dp(2)

                    Button:
                        width: dp(30)
                        height: dp(30)
                        x: self.parent.x + self.parent.width - 40
                        y: self.parent.y + self.parent.height - 40
                        font_size: sp(24)
                        background_color: 0, 0, 0, 0
                        color: 0.9, 0.9, 0.9, 1
                        markup: True
                        text: fa_icon('camera')
                        on_release: root.on_customer_photo_button_clicked()

                Label:
                    id: customer_photo_filepath_label
                    text_size: self.size
                    height: dp(30)
                    valign: "top"
                    halign: "right"
                    text: ""

                Widget:
                    size_hint_y: None
                    height: dp(30)

                Label:
                    text_size: self.size
                    height: dp(30)
                    halign: "right"
                    text: "ID / Passport:"

                Image:
                    id: customer_passport_picture_image
                    size_hint: None, None
                    pos_hint: {'right':1}
                    size: 200, 150
                    source: ''

                    canvas.before:
                        Color:
                            rgba: (0, 0, 0, 1)
                        Line:
                            rectangle: (self.x-2, self.y-2, self.width+4, self.height+4) 
                            width: dp(2)

                    Button:
                        width: dp(30)
                        height: dp(30)
                        x: self.parent.x + self.parent.width - 40
                        y: self.parent.y + self.parent.height - 40
                        font_size: sp(24)
                        background_color: 0, 0, 0, 0
                        color: 0.9, 0.9, 0.9, 1
                        markup: True
                        text: fa_icon('camera')
                        on_release: root.on_customer_passport_button_clicked()

                Label:
                    id: customer_passport_picture_filepath_label
                    text_size: self.size
                    height: dp(30)
                    valign: "top"
                    halign: "right"
                    text: ""

            BoxLayout:
                orientation: 'vertical'
                pos_hint: {'top': 1}
                size_hint_y: None
                height: self.minimum_height
                padding: dp(20)
                spacing: dp(10)

                Label:
                    text_size: self.size
                    valign: "bottom"
                    halign: "left"
                    text: "First name:"
                TextInput:
                    id: customer_first_name_input
                    text: ""
                    right: self.width
                    width: dp(340)
                    height: dp(30)
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
                    width: dp(340)
                    height: dp(30)
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
                    width: dp(340)
                    height: dp(30)
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
                    width: dp(340)
                    height: dp(30)
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
                    width: dp(340)
                    height: dp(90)
                    size_hint_x: None
                    size_hint_y: None

                Label:
                    text_size: self.size
                    valign: "bottom"
                    halign: "left"
                    text: "ATM ID:"
                TextInput:
                    id: customer_atm_id_input
                    text: ""
                    width: dp(340)
                    height: dp(30)
                    size_hint_x: None
                    size_hint_y: None

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            padding: dp(10)
            spacing: dp(2)

            RoundedButton:
                text: "save customer"
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_edit_customer_save_button_clicked()

            RoundedButton:
                text: "scan ATM ID"
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_edit_customer_scan_atm_id_button_clicked()

            RoundedButton:
                text: "print user ID card"
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_edit_customer_print_card_button_clicked()

            RoundedButton:
                text: "open folder"
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_edit_customer_open_folder_button_clicked()

            RoundedButton:
                text: "copy location"
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_edit_customer_copy_location_button_clicked()
"""

class EditCustomerScreen(screen.AppScreen):

    customer_id = None

    def scr_manager(self):
        return App.get_running_app().root.ids.scr_manager

    def take_pic_screen(self):
        return self.scr_manager().get_screen('camera_take_picture_screen')

    def populate_input_fields(self):
        Cache.remove('kv.image')
        Cache.remove('kv.texture')
        customer_info = local_storage.read_customer_info(self.customer_id) or {}
        self.ids.customer_first_name_input.text = customer_info.get('first_name') or ''
        self.ids.customer_last_name_input.text = customer_info.get('last_name') or ''
        self.ids.customer_phone_input.text = customer_info.get('phone') or ''
        self.ids.customer_email_input.text = customer_info.get('email') or ''
        self.ids.customer_address_input.text = customer_info.get('address') or ''
        self.ids.customer_atm_id_input.text = customer_info.get('atm_id') or ''
        self.ids.customer_photo_picture_image.source = ''
        self.ids.customer_photo_picture_image.source = local_storage.customer_photo_filepath(self.customer_id)
        self.ids.customer_photo_filepath_label.text = local_storage.customer_photo_filepath(self.customer_id)
        self.ids.customer_passport_picture_image.source = ''
        self.ids.customer_passport_picture_image.source = local_storage.customer_passport_filepath(self.customer_id)
        self.ids.customer_passport_picture_filepath_label.text = local_storage.customer_passport_filepath(self.customer_id)

    def save_info(self):
        local_storage.write_customer_info(dict(
            customer_id=self.customer_id,
            first_name=self.ids.customer_first_name_input.text,
            last_name=self.ids.customer_last_name_input.text,
            phone=self.ids.customer_phone_input.text,
            email=self.ids.customer_email_input.text,
            address=self.ids.customer_address_input.text,
            atm_id=self.ids.customer_atm_id_input.text,
        ))

    def on_enter(self, *args):
        self.populate_input_fields()

    def on_customer_photo_button_clicked(self, *args):
        self.camera_screen = screen_camera_take_picture.CameraTakePictureScreen(
            name='camera_take_picture_screen',
            picture_taken_callback=self.on_customer_photo_picture_ready,
            cancel_callback=self.on_customer_photo_picture_cancel,
            picture_filepath=local_storage.customer_photo_filepath(self.customer_id),
        )
        self.scr_manager().add_widget(self.camera_screen)
        self.scr_manager().current = 'camera_take_picture_screen'

    def on_customer_passport_button_clicked(self, *args):
        self.camera_screen = screen_camera_take_picture.CameraTakePictureScreen(
            name='camera_take_picture_screen',
            picture_taken_callback=self.on_customer_passport_picture_ready,
            cancel_callback=self.on_customer_passport_picture_cancel,
            picture_filepath=local_storage.customer_passport_filepath(self.customer_id),
        )
        self.scr_manager().add_widget(self.camera_screen)
        self.scr_manager().current = 'camera_take_picture_screen'

    def on_customer_photo_picture_ready(self, *args):
        Cache.remove('kv.image')
        Cache.remove('kv.texture')
        self.ids.customer_photo_picture_image.source = ''
        self.ids.customer_photo_picture_image.source = args[0]
        self.scr_manager().current = 'edit_customer_screen'
        self.scr_manager().remove_widget(self.camera_screen)

    def on_customer_photo_picture_cancel(self, *args):
        self.scr_manager().current = 'edit_customer_screen'
        self.scr_manager().remove_widget(self.camera_screen)

    def on_customer_passport_picture_ready(self, *args):
        Cache.remove('kv.image')
        Cache.remove('kv.texture')
        self.ids.customer_passport_picture_image.source = ''
        self.ids.customer_passport_picture_image.source = args[0]
        self.scr_manager().current = 'edit_customer_screen'
        self.scr_manager().remove_widget(self.camera_screen)

    def on_customer_passport_picture_cancel(self, *args):
        self.scr_manager().current = 'edit_customer_screen'
        self.scr_manager().remove_widget(self.camera_screen)

    def on_edit_customer_save_button_clicked(self, *args):
        self.save_info()
        self.scr_manager().get_screen('customers_screen').ids.customers_view.populate()
        self.scr_manager().current = 'customers_screen'

    def on_edit_customer_scan_atm_id_button_clicked(self, *args):
        self.scan_atm_id_screen = CameraScanQRScreen(
            name='camera_scan_atm_id_screen',
            scan_qr_callback=self.on_edit_customer_atm_id_scan_qr_ready,
            cancel_callback=self.on_edit_customer_atm_id_scan_qr_cancel,
        )
        self.scr_manager().add_widget(self.scan_atm_id_screen)
        self.scr_manager().current = 'camera_scan_atm_id_screen'

    def on_edit_customer_atm_id_scan_qr_ready(self, *args):
        if _Debug:
            print('on_edit_customer_customer_id_scan_qr_ready', args)
        atm_id = args[0].strip().replace('customer://', '')
        self.ids.customer_atm_id_input.text = atm_id
        self.save_info()
        self.scr_manager().current = 'edit_customer_screen'
        self.scr_manager().remove_widget(self.scan_atm_id_screen)
        self.scan_atm_id_screen = None

    def on_edit_customer_atm_id_scan_qr_cancel(self, *args):
        self.scr_manager().current = 'edit_customer_screen'
        self.scr_manager().remove_widget(self.scan_atm_id_screen)
        self.scan_atm_id_screen = None

    def on_edit_customer_print_card_button_clicked(self, *args):
        id_card = render_pdf.build_id_card(
            customer_info=local_storage.read_customer_info(self.customer_id),
            customer_photo_filepath=local_storage.customer_photo_filepath(self.customer_id),
            pdf_filepath=os.path.join(local_storage.customer_dir(self.customer_id), 'id_card.pdf'),
        )
        system.open_system_explorer(id_card['filename'], as_folder=False)

    def on_edit_customer_open_folder_button_clicked(self, *args):
        system.open_system_explorer(local_storage.customer_dir(self.customer_id))

    def on_edit_customer_copy_location_button_clicked(self, *args):
        system.copy_xclip(local_storage.customer_dir(self.customer_id))
