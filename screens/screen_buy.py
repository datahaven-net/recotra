import datetime

#------------------------------------------------------------------------------

from kivy.app import App

#------------------------------------------------------------------------------

from components.screen import AppScreen
from screens.screen_camera_scan_qr import CameraScanQRScreen
from storage import local_storage

#------------------------------------------------------------------------------

kv = """
<BuyFieldLabel@RightAlignLabel>:
    size_hint_x: None
    width: dp(200)
    valign: 'middle'


<BuyFieldInput@TextInput>:
    size_hint_x: None
    size_hint_y: None
    width: dp(360)
    height: self.minimum_height
    multiline: False


<BuyScreen>:

    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'bottom'

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .08
            padding: 10
            spacing: 2

            RoundedButton:
                id: save_customer_button
                text: "select customer"
                width: 140
                size_hint_x: None
                on_release: root.on_select_customer_button_clicked()

            RoundedButton:
                text: "clear"
                width: 140
                size_hint_x: None
                on_release: root.clean_input_fields()

            RoundedButton:
                text: "create contract"
                width: 140
                size_hint_x: None
                on_release: root.on_start_transaction_button_clicked()

    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'

        GridLayout:
            size_hint_x: None
            size_hint_y: None
            width: self.minimum_width
            height: self.minimum_height
            cols: 2
            padding: 10
            spacing: 10

            BuyFieldLabel:
                text: "first name:"
            BuyFieldInput:
                id: person_first_name_input
                text: ""

            BuyFieldLabel:
                text: "last name:"
            BuyFieldInput:
                id: person_last_name_input
                text: ""

            BuyFieldLabel:
                text: "phone:"
            BuyFieldInput:
                id: person_phone_input
                text: ""

            BuyFieldLabel:
                text: "e-mail:"
            BuyFieldInput:
                id: person_email_input
                text: ""

            BuyFieldLabel:
                text: "street address:"
            BuyFieldInput:
                id: person_address_input
                text: ""

            BuyFieldLabel:
                text: "amount (US $):"
            BuyFieldInput:
                id: usd_amount_input
                text: ""

            BuyFieldLabel:
                text: "BTC price (US $ / BTC):"
            BuyFieldInput:
                id: btc_price_input
                text: ""

            BuyFieldLabel:
                text: "BTC Amount:"
            BuyFieldInput:
                id: btc_amount_input
                text: ""

            BuyFieldLabel:
                text: "receiving BitCoin address:"
            BuyFieldInput:
                id: receive_address_input
                text: "<automatically populated from settings>"
"""

#------------------------------------------------------------------------------

class BuyScreen(AppScreen):

    selected_customer_id = None
    selected_customer_info = None

    def clean_input_fields(self):
        cur_settings = local_storage.read_settings()
        self.ids.person_first_name_input.text = ''
        self.ids.person_last_name_input.text = ''
        self.ids.person_phone_input.text = ''
        self.ids.person_email_input.text = ''
        self.ids.person_address_input.text = ''
        self.ids.usd_amount_input.text = ''
        self.ids.btc_price_input.text = ''
        self.ids.btc_amount_input.text = ''
        self.ids.receive_address_input.text = cur_settings.get('receiving_btc_address', '')
        self.selected_customer_id = None

    def populate_customer_info_fields(self, customer_info):
        self.ids.person_first_name_input.text = customer_info.get('first_name') or ''
        self.ids.person_last_name_input.text = customer_info.get('last_name') or ''
        self.ids.person_phone_input.text = customer_info.get('phone') or ''
        self.ids.person_email_input.text = customer_info.get('email') or ''
        self.ids.person_address_input.text = customer_info.get('address') or ''

    def on_pre_enter(self, *args):
        if self.selected_customer_id is None:
            self.clean_input_fields()

    def on_select_customer_button_clicked(self, *args):
        select_customer_screen = App.get_running_app().root.ids.scr_manager.get_screen('select_customer_screen')
        select_customer_screen.customer_selected_callback = self.on_customer_selected
        select_customer_screen.clear_selected_items()
        App.get_running_app().root.ids.scr_manager.current = 'select_customer_screen'

    def on_customer_selected(self, selected_customer_id):
        self.selected_customer_id = selected_customer_id
        self.selected_customer_info = local_storage.read_customer_info(self.selected_customer_id)
        self.populate_customer_info_fields(self.selected_customer_info)
        self.scr_manager().current = 'buy_screen'

    def on_receive_address_scan_qr_button_clicked(self, *args):
        self.scan_qr_screen = CameraScanQRScreen(
            name='camera_scan_qr_screen',
            scan_qr_callback=self.on_receive_address_scan_qr_ready,
            cancel_callback=self.on_receive_address_scan_qr_cancel,
        )
        self.scr_manager().add_widget(self.scan_qr_screen)
        self.scr_manager().current = 'camera_scan_qr_screen'

    def on_receive_address_scan_qr_ready(self, *args):
        self.scr_manager().current = 'buy_screen'
        self.scr_manager().remove_widget(self.scan_qr_screen)
        self.ids.receive_address_input.text = args[0]

    def on_receive_address_scan_qr_cancel(self, *args):
        self.scr_manager().current = 'buy_screen'
        self.scr_manager().remove_widget(self.scan_qr_screen)

    def on_start_transaction_button_clicked(self):
        t_now = datetime.datetime.now()
        transaction_details = {}
        transaction_details.update(dict(
            contract_type='purchase',
            usd_amount=self.ids.usd_amount_input.text,
            btc_price=self.ids.btc_price_input.text,
            btc_amount=self.ids.btc_amount_input.text,
            date=t_now.strftime("%b %d %Y"),
            time=t_now.strftime("%H:%M %p"),
            seller=dict(
                customer_id=self.selected_customer_id,
                first_name=self.ids.person_first_name_input.text,
                last_name=self.ids.person_last_name_input.text,
                btc_address=self.ids.receive_address_input.text,
                address=self.ids.person_address_input.text,
                email=self.ids.person_email_input.text,
                phone=self.ids.person_phone_input.text,
            ),
            buyer=dict(
                customer_id=None,
                first_name='ABCD',
                last_name='EFGH',
                btc_address='11223344556677889900abcdefabcdef',
                address='Anguilla, ABCD 1234',
                email='abcdefgh@gmail.com',
                phone='12345679',
            ),
        ))
        new_transaction_details = local_storage.create_new_transaction(transaction_details)
        local_storage.write_transaction(new_transaction_details['transaction_id'], new_transaction_details)
        self.scr('one_transaction_screen').transaction_id = new_transaction_details['transaction_id']
        self.scr_manager().current = 'one_transaction_screen'
