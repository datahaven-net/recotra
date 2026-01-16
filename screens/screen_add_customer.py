import datetime
import calendar
import urllib.parse

#------------------------------------------------------------------------------

from kivy.cache import Cache
from kivy.metrics import dp

#------------------------------------------------------------------------------

from components import screen
from components import dialogs
from components.webfont import fa_icon
from components.list_view import SelectableRecycleView

from lib import system

from screens import screen_camera_take_picture

from storage import local_storage

#------------------------------------------------------------------------------

months_names = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', )

kv = """
<AddCustomerScreen>:
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
                    pos_hint: {"top":1}
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
                        pos_hint: {"right":1}
                        size: 200, 150
                        source: ''

                        canvas.before:
                            Color:
                                rgba: (0, 0, 0, 1)
                            Line:
                                rectangle: (self.x-2, self.y-2, self.width+4, self.height+4) 
                                width: dp(2)

                        RoundedButton:
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
                        pos_hint: {"right":1}
                        size: 200, 150
                        source: ''

                        canvas.before:
                            Color:
                                rgba: (0, 0, 0, 1)
                            Line:
                                rectangle: (self.x-2, self.y-2, self.width+4, self.height+4) 
                                width: dp(2)

                        RoundedButton:
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

                    Widget:
                        size_hint_y: None
                        height: dp(15)

                    Label:
                        text_size: self.size
                        height: dp(30)
                        halign: "right"
                        valign: "bottom"
                        text: "Related URLs:"

                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: None, None
                        pos_hint: {'right': 1}
                        halign: "right"
                        height: dp(24)
                        width: dp(340)
                        padding: dp(0)
                        spacing: dp(5)

                        Widget:
                            size_hint: 1, None
                            height: dp(20)
                        SimpleButton:
                            id: related_urls_add_button
                            halign: "right"
                            valign: "bottom"
                            pos_hint: {'right': 1}
                            size_hint: (None, None)
                            height: dp(20)
                            width: dp(60)
                            text: "add"
                            on_release: root.on_related_urls_add_button_clicked()
                        SimpleButton:
                            id: related_urls_paste_button
                            halign: "right"
                            valign: "bottom"
                            pos_hint: {'right': 1}
                            size_hint: (None, None)
                            height: dp(20)
                            width: dp(60)
                            text: "paste"
                            on_release: root.on_related_urls_paste_button_clicked()
                        SimpleButton:
                            id: related_urls_remove_button
                            halign: "right"
                            valign: "bottom"
                            pos_hint: {'right': 1}
                            size_hint: (None, None)
                            height: dp(20)
                            width: dp(60)
                            text: "remove"
                            disabled: True
                            on_release: root.on_related_urls_remove_button_clicked()
                        SimpleButton:
                            id: related_urls_open_button
                            halign: "right"
                            valign: "bottom"
                            pos_hint: {'right': 1}
                            size_hint: (None, None)
                            height: dp(20)
                            width: dp(60)
                            text: "open"
                            disabled: True
                            on_release: root.on_related_urls_open_button_clicked()

                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: None, None
                        pos_hint: {'right': 1}
                        height: dp(80)
                        width: dp(330)
                        padding: dp(0)

                        RelatedURLsView:
                            id: related_urls_view
                            size_hint: 1, 1

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
                        text: "First and middle names:"
                    TextInput:
                        id: customer_first_name_input
                        text: ""
                        right: self.width
                        width: dp(250)
                        height: dp(30)
                        size_hint_x: None
                        size_hint_y: None
                        multiline: False
                        write_tab: False

                    Label:
                        text_size: self.size
                        valign: "bottom"
                        halign: "left"
                        text: "Last name:"
                    TextInput:
                        id: customer_last_name_input
                        text: ""
                        width: dp(250)
                        height: dp(30)
                        size_hint_x: None
                        size_hint_y: None
                        multiline: False
                        write_tab: False

                    Label:
                        text_size: self.size
                        valign: "bottom"
                        halign: "left"
                        text: "Phone:"
                    TextInput:
                        id: customer_phone_input
                        text: ""
                        width: dp(250)
                        height: dp(30)
                        size_hint_x: None
                        size_hint_y: None
                        multiline: False
                        write_tab: False

                    Label:
                        text_size: self.size
                        valign: "bottom"
                        halign: "left"
                        text: "E-mail:"
                    TextInput:
                        id: customer_email_input
                        text: ""
                        width: dp(250)
                        height: dp(30)
                        size_hint_x: None
                        size_hint_y: None
                        multiline: False
                        write_tab: False

                    Label:
                        text_size: self.size
                        valign: "bottom"
                        halign: "left"
                        text: "Address:"
                    TextInput:
                        id: customer_address_input
                        text: ""
                        width: dp(250)
                        height: dp(60)
                        size_hint_x: None
                        size_hint_y: None
                        multiline: True
                        write_tab: False

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
                text: "Save Customer"
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_add_customer_save_button_clicked()

            RoundedButton:
                text: "Google customer"
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_google_customer_button_clicked()
""" % (
    ','.join(["'%s'" % y for y in range(datetime.date.today().year+25, datetime.date.today().year-10, -1)]),
    ','.join(["'%s'" % m for m in months_names]),
    ','.join(["'%s'" % d for d in range(1, 31+1)]),
)

#------------------------------------------------------------------------------

class RelatedURLsView(SelectableRecycleView):

    def __init__(self, **kwargs):
        super(RelatedURLsView, self).__init__(**kwargs)
        self.data_copy = []

    def populate(self):
        self.data = []
        self.data_copy = list(self.data)
        self.scroll_x = 0
        self.scroll_y = 0

    def on_selection_applied(self, item, index, is_selected, prev_selected):
        root = self.parent.parent.parent.parent.parent.parent
        if is_selected:
            root.ids.related_urls_remove_button.disabled = False
            root.ids.related_urls_open_button.disabled = False
        else:
            root.ids.related_urls_remove_button.disabled = True
            root.ids.related_urls_open_button.disabled = True

#------------------------------------------------------------------------------

class AddCustomerScreen(screen.AppScreen):

    new_customer_id = None
    camera_on = False

    def take_pic_screen(self):
        return self.scr_manager().get_screen('camera_take_picture_screen')

    def clean_input_fields(self):
        Cache.remove('kv.image')
        Cache.remove('kv.texture')
        self.ids.customer_first_name_input.text = ''
        self.ids.customer_last_name_input.text = ''
        self.ids.customer_phone_input.text = ''
        self.ids.customer_email_input.text = ''
        self.ids.customer_address_input.text = ''
        self.ids.customer_photo_picture_image.source = ''
        self.ids.customer_passport_picture_image.source = ''
        self.ids.select_id_expire_year_button.text = '-'
        self.ids.select_id_expire_month_button.text = '-'
        self.ids.select_id_expire_day_button.text = '-'
        self.ids.select_risk_rating_button.text = 'low'
        self.ids.related_urls_view.data = []

    def on_add_customer_save_button_clicked(self, *args):
        year = self.ids.select_id_expire_year_button.text
        month = self.ids.select_id_expire_month_button.text
        day = self.ids.select_id_expire_day_button.text
        if year == '-' or month == '-' or day == '-':
            dialogs.show_one_button_dialog(
                title='Warning',
                message='ID / Passport expiration Date is mandatory',
            )
            return
        if not self.ids.related_urls_view.data:
            dialogs.show_one_button_dialog(
                title='Warning',
                message='Must first perform Google search of the customer and provide some related URLs',
            )
            return
        month_pos = months_names.index(month) + 1
        local_storage.write_customer_info(dict(
            customer_id=self.new_customer_id,
            first_name=self.ids.customer_first_name_input.text,
            last_name=self.ids.customer_last_name_input.text,
            phone=self.ids.customer_phone_input.text,
            email=self.ids.customer_email_input.text,
            address=self.ids.customer_address_input.text,
            atm_id='',
            id_expire_date='%s-%s-%s' % (year, str(month_pos), day),
            risk_rating=self.ids.select_risk_rating_button.text,
            is_blocked=False,
            text_notes='',
            related_urls=[d['url'] for d in self.ids.related_urls_view.data],
        ))
        self.new_customer_id = None
        self.camera_on = False
        self.scr_manager().get_screen('customers_screen').ids.customers_view.populate()
        self.scr_manager().current = 'customers_screen'

    def on_enter(self, *args):
        # print('on_enter', args, self.new_customer_id, self.camera_on)
        if self.camera_on:
            self.camera_on = False
            return
        if self.new_customer_id is not None:
            local_storage.erase_customer_info(self.new_customer_id)
            self.new_customer_id = None
            self.new_customer_id = local_storage.create_new_customer_info()
            self.clean_input_fields()
        else:
            self.new_customer_id = local_storage.create_new_customer_info()
            self.clean_input_fields()

    def on_leave(self, *args):
        # print('on_leave', args, self.new_customer_id, self.camera_on)
        if self.new_customer_id is not None:
            if not self.camera_on:
                local_storage.erase_customer_info(self.new_customer_id)
                self.new_customer_id = None

    def on_customer_photo_button_clicked(self, *args):
        self.camera_on = True
        self.camera_screen = screen_camera_take_picture.CameraTakePictureScreen(
            name='camera_take_picture_screen',
            picture_taken_callback=self.on_customer_photo_picture_ready,
            cancel_callback=self.on_customer_photo_picture_cancel,
            picture_filepath=local_storage.customer_photo_filepath(self.new_customer_id), 
        )
        self.scr_manager().add_widget(self.camera_screen)
        self.scr_manager().current = 'camera_take_picture_screen'

    def on_customer_passport_button_clicked(self, *args):
        self.camera_on = True
        self.camera_screen = screen_camera_take_picture.CameraTakePictureScreen(
            name='camera_take_picture_screen',
            picture_taken_callback=self.on_customer_passport_picture_ready,
            cancel_callback=self.on_customer_passport_picture_cancel,
            picture_filepath=local_storage.customer_passport_filepath(self.new_customer_id),
        )
        self.scr_manager().add_widget(self.camera_screen)
        self.scr_manager().current = 'camera_take_picture_screen'

    def on_customer_photo_picture_ready(self, *args):
        self.ids.customer_photo_picture_image.source = args[0]
        self.scr_manager().current = 'add_customer_screen'
        self.scr_manager().remove_widget(self.camera_screen)
        # self.camera_on = False

    def on_customer_photo_picture_cancel(self, *args):
        self.ids.customer_photo_picture_image.source = ''
        self.scr_manager().current = 'add_customer_screen'
        self.scr_manager().remove_widget(self.camera_screen)

    def on_customer_passport_picture_ready(self, *args):
        self.ids.customer_passport_picture_image.source = args[0]
        self.scr_manager().current = 'add_customer_screen'
        self.scr_manager().remove_widget(self.camera_screen)
        # self.camera_on = False

    def on_customer_passport_picture_cancel(self, *args):
        self.ids.customer_passport_picture_image.source = ''
        self.scr_manager().current = 'add_customer_screen'
        self.scr_manager().remove_widget(self.camera_screen)

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

    def on_select_risk_rating_button_clicked(self, *args):
        pass

    def on_related_urls_add_button_clicked(self, *args):
        dialogs.open_text_input_dialog(
            title=f'Customer related URL',
            dialog_size=(dp(600), dp(140), ),
            button_confirm='add',
            button_cancel='cancel',
            multiline=False,
            cb=self.on_add_related_url_dialog_result,
        )

    def on_add_related_url_dialog_result(self, url):
        if url:
            found = False
            for d in self.ids.related_urls_view.data:
                if d['url'] == url:
                    found = True
                    break
            if not found:
                self.ids.related_urls_view.data.append({'url': url})

    def on_related_urls_paste_button_clicked(self, *args):
        url = system.paste_xclip()
        if url:
            found = False
            for d in self.ids.related_urls_view.data:
                if d['url'] == url:
                    found = True
                    break
            if not found:
                self.ids.related_urls_view.data.append({'url': url})

    def on_related_urls_remove_button_clicked(self, *args):
        if self.ids.related_urls_view.selected_item:
            for d in self.ids.related_urls_view.data:
                if d['url'] == self.ids.related_urls_view.selected_item.url:
                    self.ids.related_urls_view.data.remove(d)
                    self.ids.related_urls_remove_button.disabled = True
                    self.ids.related_urls_open_button.disabled = True
                    break

    def on_related_urls_open_button_clicked(self, *args):
        if self.ids.related_urls_view.selected_item:
            system.open_webbrowser(self.ids.related_urls_view.selected_item.url)
