import datetime

#------------------------------------------------------------------------------

from kivy.app import App
from screens.screen_camera_scan_qr import CameraScanQRScreen

#------------------------------------------------------------------------------

from lib import coinmarketcap_client

from components.screen import AppScreen

from storage import local_storage

#------------------------------------------------------------------------------

kv = """
<SellFieldLabel@RightAlignLabel>:
    size_hint_x: None
    width: dp(200)
    valign: 'middle'


<SellFieldInput@TextInput>:
    size_hint_x: None
    size_hint_y: None
    width: dp(360)
    height: self.minimum_height
    multiline: False


<SellScreen>:

    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'bottom'

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .08
            padding: 10
            spacing: 2

            RoundedButton:
                id: select_customer_button
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

            SellFieldLabel:
                text: "first name:"
            SellFieldInput:
                id: person_first_name_input
                text: ""

            SellFieldLabel:
                text: "last name:"
            SellFieldInput:
                id: person_last_name_input
                text: ""

            SellFieldLabel:
                text: "phone:"
            SellFieldInput:
                id: person_phone_input
                text: ""

            SellFieldLabel:
                text: "e-mail:"
            SellFieldInput:
                id: person_email_input
                text: ""

            SellFieldLabel:
                text: "street address:"
            SellFieldInput:
                id: person_address_input
                text: ""

            SellFieldLabel:
                text: "Amount (US $):"
            SellFieldInput:
                id: usd_amount_input
                text: ""

            SellFieldLabel:
                text: "BTC price (US $ / BTC):"
            SellFieldInput:
                id: btc_price_input
                text: ""

            SellFieldLabel:
                text: "BTC amount:"
            SellFieldInput:
                id: btc_amount_input
                text: ""

            SellFieldLabel:
                text: "receiving BitCoin address:"
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: self.minimum_height
                SellFieldInput:
                    id: receive_address_input
                    text: ""
                RoundedButton:
                    size_hint: None, 1
                    width: self.texture_size[0]
                    text: "  scan  "
                    on_release: root.on_receive_address_scan_qr_button_clicked()
"""

#------------------------------------------------------------------------------

class SellScreen(AppScreen):

    selected_customer_id = None
    selected_customer_info = None

    def clean_input_fields(self):
        self.selected_customer_id = None
        self.ids.person_first_name_input.text = ''
        self.ids.person_last_name_input.text = ''
        self.ids.person_phone_input.text = ''
        self.ids.person_email_input.text = ''
        self.ids.person_address_input.text = ''
        self.ids.usd_amount_input.text = ''
        self.ids.btc_price_input.text = ''
        self.ids.btc_amount_input.text = ''
        self.ids.receive_address_input.text = ''
        cur_settings = local_storage.read_settings()
        coinmarketcap_api_key = cur_settings.get('coinmarketcap_api_key', '')
        if coinmarketcap_api_key:
            coinmarketcap_response = coinmarketcap_client.cryptocurrency_listings(
                api_key=coinmarketcap_api_key, start=1, limit=1, convert='USD',
            )
            if coinmarketcap_response:
                try:
                    btc_usd_price = coinmarketcap_response['data'][0]['quote']['USD']['price']
                except:
                    print('failed coinmarketcap response:', coinmarketcap_response)
                    btc_usd_price = None
                if btc_usd_price is not None:
                    self.ids.btc_price_input.text = '%.2f' % btc_usd_price

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
        self.scr_manager().current = 'sell_screen'

    def on_receive_address_scan_qr_button_clicked(self, *args):
        self.scan_qr_screen = CameraScanQRScreen(
            name='camera_scan_qr_screen',
            scan_qr_callback=self.on_receive_address_scan_qr_ready,
            cancel_callback=self.on_receive_address_scan_qr_cancel,
        )
        self.scr_manager().add_widget(self.scan_qr_screen)
        self.scr_manager().current = 'camera_scan_qr_screen'

    def on_receive_address_scan_qr_ready(self, *args):
        self.scr_manager().current = 'sell_screen'
        self.scr_manager().remove_widget(self.scan_qr_screen)
        self.ids.receive_address_input.text = args[0]

    def on_receive_address_scan_qr_cancel(self, *args):
        self.scr_manager().current = 'sell_screen'
        self.scr_manager().remove_widget(self.scan_qr_screen)

    def on_start_transaction_button_clicked(self):
        t_now = datetime.datetime.now()
        transaction_details = {}
        transaction_details.update(dict(
            contract_type='sales',
            usd_amount=self.ids.usd_amount_input.text,
            btc_price=self.ids.btc_price_input.text,
            btc_amount=self.ids.btc_amount_input.text,
            date=t_now.strftime("%b %d %Y"),
            time=t_now.strftime("%H:%M %p"),
            seller=dict(
                customer_id=None,
                first_name='ABCD',
                last_name='EFGH',
                btc_address='11223344556677889900abcdefabcdef',
                address='Anguilla, ABCD 1234',
                email='abcdefgh@gmail.com',
                phone='12345679',
            ),
            buyer=dict(
                customer_id=self.selected_customer_id,
                first_name=self.ids.person_first_name_input.text,
                last_name=self.ids.person_last_name_input.text,
                btc_address=self.ids.receive_address_input.text,
                address=self.ids.person_address_input.text,
                email=self.ids.person_email_input.text,
                phone=self.ids.person_phone_input.text,
            ),
        ))
        new_transaction_details = local_storage.create_new_transaction(transaction_details)
        local_storage.write_transaction(new_transaction_details['transaction_id'], new_transaction_details)
        self.scr('one_transaction_screen').transaction_id = new_transaction_details['transaction_id']
        self.scr_manager().current = 'one_transaction_screen'
