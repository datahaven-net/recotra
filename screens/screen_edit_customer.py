import os
import datetime
import calendar
import urllib.parse

#------------------------------------------------------------------------------

from kivy.cache import Cache

#------------------------------------------------------------------------------

from components import screen
from components import dialogs

from lib import render_pdf
from lib import system

from storage import local_storage

from screens import screen_camera_take_picture
from screens.screen_camera_scan_qr import CameraScanQRScreen

#------------------------------------------------------------------------------

_Debug = False

#------------------------------------------------------------------------------

months_names = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', )

kv = """
<EditCustomerScreen>:

    BoxLayout:
        orientation: 'vertical'

        ScrollView:
            scroll_type: ['bars']
            bar_width: dp(15)
            bar_color: .2,.5,.8,1
            bar_inactive_color: .1,.4,.7,1
            effect_cls: "ScrollEffect"
            do_scroll_x: False
            always_overscroll: False

            BoxLayout:
                orientation: 'horizontal'
                size_hint: 1, None
                height: self.minimum_height
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

                    Widget:
                        size_hint_y: None
                        height: dp(30)

                    Label:
                        text_size: self.size
                        height: dp(30)
                        halign: "right"
                        text: "ID / Passport expiration Date:"

                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: 1, None
                        height: dp(22)

                        Widget:
                            size_hint: 1, None
                            height: dp(20)

                        CompactSpinner:
                            id: select_id_expire_year_button
                            width: dp(78)
                            text: '-'
                            values: '-', %s
                            on_text: root.on_select_id_expire_year_button_clicked()

                        CompactSpinner:
                            id: select_id_expire_month_button
                            width: dp(78)
                            text: '-'
                            values: '-', %s
                            on_text: root.on_select_id_expire_month_button_clicked()

                        CompactSpinner:
                            id: select_id_expire_day_button
                            width: dp(78)
                            text: '-'
                            values: '-', %s
                            on_text: root.on_select_id_expire_day_button_clicked()

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

                    Label:
                        text_size: self.size
                        valign: "bottom"
                        halign: "left"
                        text: ""
                    Label:
                        text_size: self.size
                        valign: "bottom"
                        halign: "left"
                        text: "Transactions limit per month in dollars:"
                    TextInput:
                        id: customer_limit_transactions_input
                        text: ""
                        width: dp(340)
                        height: dp(30)
                        size_hint_x: None
                        size_hint_y: None
                    Label:
                        id: this_month_sold_usd
                        height: dp(20)
                        size_hint_y: None
                        text_size: self.size
                        valign: "bottom"
                        halign: "left"
                        text: "This month, sold BTC for a total of $0"
                    Label:
                        id: this_month_bought_usd
                        height: dp(20)
                        size_hint_y: None
                        text_size: self.size
                        valign: "bottom"
                        halign: "left"
                        text: "This month, bought BTC for a total of $0"

                    Widget:
                        size_hint_y: None
                        height: dp(4)

                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: None, None
                        height: dp(24)
                        width: dp(340)

                        Label:
                            text_size: self.size
                            size_hint: (None, None)
                            width: dp(84)
                            height: dp(24)
                            halign: "left"
                            text: "Risk rating: "

                        CompactSpinner:
                            id: select_risk_rating_button
                            width: dp(72)
                            text: 'low'
                            values: 'low', 'medium', 'high'
                            on_text: root.on_select_risk_rating_button_clicked()

                        Widget:
                            size_hint: 1, None
                            height: dp(22)

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

            RoundedButton:
                text: "Google customer"
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_google_customer_button_clicked()

""" % (
    ','.join(["'%s'" % y for y in range(datetime.date.today().year, datetime.date.today().year-50, -1)]),
    ','.join(["'%s'" % m for m in months_names]),
    ','.join(["'%s'" % d for d in range(1, 31+1)]),
)

class EditCustomerScreen(screen.AppScreen):

    customer_id = None

    def take_pic_screen(self):
        return self.scr_manager().get_screen('camera_take_picture_screen')

    def populate_input_fields(self):
        Cache.remove('kv.image')
        Cache.remove('kv.texture')
        customer_info = local_storage.read_customer_info(self.customer_id) or {}
        bought, sold = local_storage.calculate_customer_transactions_this_month(self.customer_id)
        id_expire_date = customer_info.get('id_expire_date') or ''
        if id_expire_date:
            year, month, day = id_expire_date.split('-')
            self.ids.select_id_expire_year_button.text = year
            self.ids.select_id_expire_month_button.text = months_names[int(month) - 1]
            self.ids.select_id_expire_day_button.text = day
        else:
            self.ids.select_id_expire_year_button.text = '-'
            self.ids.select_id_expire_month_button.text = '-'
            self.ids.select_id_expire_day_button.text = '-'
        self.ids.customer_first_name_input.text = customer_info.get('first_name') or ''
        self.ids.customer_last_name_input.text = customer_info.get('last_name') or ''
        self.ids.customer_phone_input.text = customer_info.get('phone') or ''
        self.ids.customer_email_input.text = customer_info.get('email') or ''
        self.ids.customer_address_input.text = customer_info.get('address') or ''
        self.ids.customer_atm_id_input.text = customer_info.get('atm_id') or ''
        self.ids.customer_limit_transactions_input.text = customer_info.get('limit_transactions') or '5000'
        self.ids.customer_photo_picture_image.source = ''
        self.ids.customer_photo_picture_image.source = local_storage.customer_photo_filepath(self.customer_id)
        self.ids.customer_photo_filepath_label.text = local_storage.customer_photo_filepath(self.customer_id)
        self.ids.customer_passport_picture_image.source = ''
        self.ids.customer_passport_picture_image.source = local_storage.customer_passport_filepath(self.customer_id)
        self.ids.customer_passport_picture_filepath_label.text = local_storage.customer_passport_filepath(self.customer_id)
        self.ids.this_month_sold_usd.text = f'This month, sold BTC for a total of [b]${sold}[/b]'
        self.ids.this_month_bought_usd.text = f'This month, bought BTC for a total of [b]${bought}[/b]'
        self.ids.select_risk_rating_button.text = customer_info.get('risk_rating') or 'low'

    def save_info(self):
        year = self.ids.select_id_expire_year_button.text
        month = self.ids.select_id_expire_month_button.text
        day = self.ids.select_id_expire_day_button.text
        month_pos = months_names.index(month) + 1
        local_storage.write_customer_info(dict(
            customer_id=self.customer_id,
            first_name=self.ids.customer_first_name_input.text,
            last_name=self.ids.customer_last_name_input.text,
            phone=self.ids.customer_phone_input.text,
            email=self.ids.customer_email_input.text,
            address=self.ids.customer_address_input.text,
            atm_id=self.ids.customer_atm_id_input.text,
            limit_transactions=self.ids.customer_limit_transactions_input.text,
            id_expire_date='%s-%s-%s' % (year, str(month_pos), day),
            risk_rating=self.ids.select_risk_rating_button.text,
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
        year = self.ids.select_id_expire_year_button.text
        month = self.ids.select_id_expire_month_button.text
        day = self.ids.select_id_expire_day_button.text
        if year == '-' or month == '-' or day == '-':
            dialogs.show_one_button_dialog(
                title='Warning',
                message='ID / Passport expiration Date is mandatory',
            )
            return
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

    def on_google_customer_button_clicked(self, *args):
        if self.ids.customer_first_name_input.text and self.ids.customer_last_name_input.text:
            system.open_webbrowser('https://www.google.ru/search?q=%s+%s+Anguilla' % (
                urllib.parse.quote_plus(self.ids.customer_first_name_input.text),
                urllib.parse.quote_plus(self.ids.customer_last_name_input.text),
            ))
            system.open_webbrowser('https://www.google.ru/search?q=%s+%s+Facebook+Anguilla' % (
                urllib.parse.quote_plus(self.ids.customer_first_name_input.text),
                urllib.parse.quote_plus(self.ids.customer_last_name_input.text),
            ))

    def on_select_id_expire_year_button_clicked(self, *args):
        year = self.ids.select_id_expire_year_button.text
        month = self.ids.select_id_expire_month_button.text
        day = self.ids.select_id_expire_day_button.text
        if year != '-' and month != '-':
            month_pos = months_names.index(month) + 1
            num_days = calendar.monthrange(int(year), month_pos)[1]
            days_range = [str(d) for d in range(1, num_days+1)]
            if day != '-' and day not in days_range:
                self.ids.select_id_expire_day_button.text = '-'
            self.ids.select_id_expire_day_button.values = days_range
        else:
            self.ids.select_id_expire_day_button.values = [str(d) for d in range(1, 31+1)]

    def on_select_id_expire_month_button_clicked(self, *args):
        year = self.ids.select_id_expire_year_button.text
        month = self.ids.select_id_expire_month_button.text
        day = self.ids.select_id_expire_day_button.text
        if year != '-' and month != '-':
            month_pos = months_names.index(month) + 1
            num_days = calendar.monthrange(int(year), month_pos)[1]
            days_range = [str(d) for d in range(1, num_days+1)]
            if day != '-' and day not in days_range:
                self.ids.select_id_expire_day_button.text = '-'
            self.ids.select_id_expire_day_button.values = days_range
        else:
            self.ids.select_id_expire_day_button.values = [str(d) for d in range(1, 31+1)]

    def on_select_id_expire_day_button_clicked(self, *args):
        pass

    def on_select_risk_rating_button_clicked(self, *args):
        pass
