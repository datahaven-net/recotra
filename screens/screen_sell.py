import datetime

#------------------------------------------------------------------------------

from kivy.app import App
from kivy.clock import Clock
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
            cols: 1
            padding: 10
            spacing: 10

            Label:
                size_hint: 1, None
                height: dp(40)
                font_size: sp(20)
                text: "Customer buying BTC from Bitcoin.ai"

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
                    text: "amount (US $):"
                SellFieldInput:
                    id: usd_amount_input
                    text: ""
                    on_text: root.on_usd_amount_input_changed(self.text)

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
                    on_text: root.on_btc_amount_input_changed(self.text)

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
    populate_usd_amount_task = None
    populate_btc_amount_task = None

    def clean_input_fields(self):
        self.selected_customer_id = None
        self.ids.person_first_name_input.text = ''
        self.ids.person_last_name_input.text = ''
        self.ids.person_phone_input.text = ''
        self.ids.person_email_input.text = ''
        self.ids.person_address_input.text = ''
        self.ids.usd_amount_input.text = '0.0'
        self.ids.btc_price_input.text = '0.0'
        self.ids.btc_amount_input.text = '0.0'
        self.ids.receive_address_input.text = ''

    def populate_btc_usd_price(self):
        cur_settings = local_storage.read_settings()
        coinmarketcap_api_key = cur_settings.get('coinmarketcap_api_key', '')
        if coinmarketcap_api_key:
            coinmarketcap_client.cryptocurrency_listings(
                api_key=coinmarketcap_api_key,
                start=1,
                limit=1,
                convert='USD',
                cb=self.on_coinmarketcap_response,
            )

    def populate_customer_info_fields(self, customer_info):
        self.ids.person_first_name_input.text = customer_info.get('first_name') or ''
        self.ids.person_last_name_input.text = customer_info.get('last_name') or ''
        self.ids.person_phone_input.text = customer_info.get('phone') or ''
        self.ids.person_email_input.text = customer_info.get('email') or ''
        self.ids.person_address_input.text = customer_info.get('address') or ''

    def on_pre_enter(self, *args):
        if self.selected_customer_id is None:
            self.clean_input_fields()
            self.populate_btc_usd_price()

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
        qr = args[0].strip()
        if qr.lower().startswith('bitcoin:'):
            qr = qr[8:]
        if qr.count('?'):
            qr, _, _ = qr.partition('?')
        self.ids.receive_address_input.text = args[0]

    def on_receive_address_scan_qr_cancel(self, *args):
        self.scr_manager().current = 'sell_screen'
        self.scr_manager().remove_widget(self.scan_qr_screen)

    def on_coinmarketcap_response(self, request, response):
        if response:
            try:
                btc_usd_price = float(response['data'][0]['quote']['USD']['price'])
            except:
                btc_usd_price = None
            if btc_usd_price is not None:
                self.ids.btc_price_input.text = '%.2f' % btc_usd_price

    def on_usd_amount_input_changed(self, new_text):
        if not new_text:
            self.populate_btc_amount_task = None
            return
        if self.populate_btc_amount_task:
            Clock.unschedule(self.populate_btc_amount_task)
            self.populate_btc_amount_task = Clock.schedule_once(self.on_usd_amount_input_changed_earlier, 0.1)
        else:
            self.populate_btc_amount_task = Clock.schedule_once(self.on_usd_amount_input_changed_earlier, 0.1)

    def on_btc_amount_input_changed(self, new_text):
        if not new_text:
            self.populate_usd_amount_task = None
            return
        if self.populate_usd_amount_task:
            Clock.unschedule(self.populate_usd_amount_task)
            self.populate_usd_amount_task = Clock.schedule_once(self.on_btc_amount_input_changed_earlier, 0.1)
        else:
            self.populate_usd_amount_task = Clock.schedule_once(self.on_btc_amount_input_changed_earlier, 0.1)

    def on_usd_amount_input_changed_earlier(self, *args):
        self.populate_btc_amount_task = None
        if not self.ids.usd_amount_input.focused:
            return
        cur_settings = local_storage.read_settings()
        try:
            usd_amount_current = float(self.ids.usd_amount_input.text)
            btc_usd_commission_percent = float(cur_settings.get('btc_usd_commission_percent', '0.0'))
            btc_price_current = float(self.ids.btc_price_input.text)
            factor = 100.0 / (100.0 + btc_usd_commission_percent)
        except:
            return
        if btc_price_current:
            t = ('%.6f' % round(factor * usd_amount_current / btc_price_current, 6)).rstrip('0')
            if t.endswith('.'):
                t += '0'
            self.ids.btc_amount_input.text = t

    def on_btc_amount_input_changed_earlier(self, *args):
        self.populate_usd_amount_task = None
        if not self.ids.btc_amount_input.focused:
            return
        cur_settings = local_storage.read_settings()
        try:
            btc_amount_current = float(self.ids.btc_amount_input.text)
            btc_usd_commission_percent = float(cur_settings.get('btc_usd_commission_percent', '0.0'))
            btc_price_current = float(self.ids.btc_price_input.text)
            factor = (100.0 + btc_usd_commission_percent) / 100.0 
        except:
            return
        self.ids.usd_amount_input.text = '%.2f' % round(factor * btc_amount_current * btc_price_current, 2)

    def on_start_transaction_button_clicked(self):
        cur_settings = local_storage.read_settings()
        t_now = datetime.datetime.now()
        transaction_details = {}
        transaction_details.update(dict(
            contract_type='sales',
            usd_amount=self.ids.usd_amount_input.text,
            btc_price=self.ids.btc_price_input.text,
            btc_amount=self.ids.btc_amount_input.text,
            fee_percent=str(float(cur_settings.get('btc_usd_commission_percent', '0.0'))),
            date=t_now.strftime("%b %d %Y"),
            time=t_now.strftime("%H:%M %p"),
            seller=dict(
                customer_id=None,
                first_name=cur_settings.get('business_owner_first_name', ''),
                last_name=cur_settings.get('business_owner_last_name', ''),
                address=cur_settings.get('business_address', ''),
                email=cur_settings.get('business_email', ''),
                phone=cur_settings.get('business_phone', ''),
                btc_address=cur_settings.get('receiving_btc_address', ''),
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
            company_name=cur_settings.get('business_company_name', ''),
        ))
        new_transaction_details = local_storage.create_new_transaction(transaction_details)
        local_storage.write_transaction(new_transaction_details['transaction_id'], new_transaction_details)
        self.scr('one_transaction_screen').transaction_id = new_transaction_details['transaction_id']
        self.scr_manager().current = 'one_transaction_screen'
