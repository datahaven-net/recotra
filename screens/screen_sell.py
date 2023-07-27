import datetime

#------------------------------------------------------------------------------

from kivy.clock import Clock

#------------------------------------------------------------------------------

from lib import coinmarketcap_client
from lib import btc_util

from components.screen import AppScreen
from components import dialogs

from screens.screen_camera_scan_qr import CameraScanQRScreen

from storage import local_storage

#------------------------------------------------------------------------------

_Debug = False

#------------------------------------------------------------------------------

kv = """
<SellFieldLabel@RightAlignLabel>:
    size_hint_x: None
    width: dp(190)
    valign: 'middle'


<SellFieldInput@TextInput>:
    size_hint_x: None
    size_hint_y: None
    width: dp(510)
    height: self.minimum_height
    multiline: False
    write_tab: False


<SellScreen>:

    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'bottom'

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .08
            padding: dp(10)
            spacing: dp(2)

            RoundedButton:
                id: select_customer_button
                text: "select customer"
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_select_customer_button_clicked()

            RoundedButton:
                id: scan_customer_id_button
                text: "scan customer ID"
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_scan_customer_id_button_clicked()

            RoundedButton:
                text: "clear"
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_clear_button_clicked()

            RoundedButton:
                text: "create contract"
                width: self.texture_size[0] + dp(20)
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
            padding: dp(10)
            spacing: dp(10)

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
                padding: dp(10)
                spacing: dp(10)

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
                        width: self.texture_size[0] + dp(16)
                        text: fa_icon('camera')
                        on_release: root.on_receive_address_scan_qr_button_clicked()
"""

#------------------------------------------------------------------------------

class SellScreen(AppScreen):

    selected_customer_id = None
    selected_customer_info = None
    populate_usd_amount_task = None
    populate_btc_amount_task = None
    populated_receive_address_qr_scan = None
    populated_customer_id_qr_scan = None

    def clean_input_fields(self):
        if _Debug:
            print('clean_input_fields')
        self.selected_customer_id = None
        self.ids.person_first_name_input.text = ''
        self.ids.person_last_name_input.text = ''
        self.ids.person_phone_input.text = ''
        self.ids.person_email_input.text = ''
        self.ids.person_address_input.text = ''
        self.ids.usd_amount_input.text = '0.0'
        # self.ids.btc_price_input.text = '0.0'
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

    def populate_usd_amount_from_btc_amount(self):
        # USD_amount = ((100.0 + BTC_USD_commission) / 100.0) * BTC_amount * BTC_price_coinmarkercap
        cur_settings = local_storage.read_settings()
        try:
            btc_amount_current = float(self.ids.btc_amount_input.text)
            btc_usd_commission_percent = float(cur_settings.get('btc_usd_commission_percent', '0.0'))
            btc_price_current = float(self.ids.btc_price_input.text)
            rate_for_this_contract = btc_price_current * (1.0 + btc_usd_commission_percent / 100.0)
        except:
            import traceback
            traceback.print_exc()
            return
        self.ids.usd_amount_input.text = '%.2f' % round(btc_amount_current * rate_for_this_contract, 2)

    def populate_btc_amount_from_usd_amount(self):
        cur_settings = local_storage.read_settings()
        try:
            usd_amount_current = float(self.ids.usd_amount_input.text)
            btc_usd_commission_percent = float(cur_settings.get('btc_usd_commission_percent', '0.0'))
            btc_price_current = float(self.ids.btc_price_input.text)
            rate_for_this_contract = btc_price_current * (1.0 + btc_usd_commission_percent / 100.0)
        except:
            import traceback
            traceback.print_exc()
            return
        if btc_price_current:
            t = ('%.6f' % round(usd_amount_current / rate_for_this_contract, 6)).rstrip('0')
            if t.endswith('.'):
                t += '0'
            self.ids.btc_amount_input.text = t

    def populate_customer_id(self, inp):
        inp = inp.replace('customer://', '')
        atm_id = None
        customer_id = None
        if inp.count(':'):
            customer_id, _, atm_id = inp.partition(':')
        else:
            if inp.count('-'):
                atm_id = inp
            else:
                customer_id = inp
        if _Debug:
            print('populate_customer_id customer_id=%r atm_id=%r' % (customer_id, atm_id, ))
        if customer_id:
            try:
                customer_id = int(customer_id)
            except:
                if _Debug:
                    print('populate_customer_id failed to parse customer ID: %r' % inp)
                return
        if atm_id is not None:
            for customer_info in local_storage.load_customers_list():
                if customer_info.get('atm_id') == atm_id:
                    customer_id = customer_info.get('customer_id')
                    try:
                        customer_id = int(customer_id)
                    except:
                        if _Debug:
                            print('populate_customer_id failed to read customer ID found from atm ID: %r' % customer_info)
                        return
                    if _Debug:
                        print('populate_customer_id found customer %d by atm ID: %r' % (customer_id, atm_id, ))
                    break
        if customer_id is not None:
            self.select_customer(customer_id)

    def select_customer(self, customer_id):
        if _Debug:
            print('select_customer', customer_id)
        customer_info = local_storage.read_customer_info(customer_id)
        if customer_info:
            self.selected_customer_id = customer_id
            self.selected_customer_info = customer_info
            self.populate_customer_info_fields(self.selected_customer_info)

    #------------------------------------------------------------------------------

    def on_enter(self, *args):
        if self.populated_customer_id_qr_scan:
            self.populate_customer_id(self.populated_customer_id_qr_scan)
            self.populated_customer_id_qr_scan = None
        if self.selected_customer_id is None:
            self.clean_input_fields()
        self.populate_btc_usd_price()
        if self.populated_receive_address_qr_scan:
            self.ids.receive_address_input.text = btc_util.parse_btc_url(self.populated_receive_address_qr_scan)['address']
            self.populated_receive_address_qr_scan = None

    #------------------------------------------------------------------------------

    def on_select_customer_button_clicked(self, *args):
        select_customer_screen = self.scr_manager().get_screen('select_customer_screen')
        select_customer_screen.customer_selected_callback = self.on_customer_selected
        select_customer_screen.clear_selected_items()
        self.scr_manager().current = 'select_customer_screen'

    def on_customer_selected(self, selected_customer_id):
        self.select_customer(selected_customer_id)
        self.scr_manager().current = 'sell_screen'

    #------------------------------------------------------------------------------

    def on_scan_customer_id_button_clicked(self, *args):
        self.scan_customer_id_screen = CameraScanQRScreen(
            name='camera_scan_customer_id_screen',
            scan_qr_callback=self.on_customer_id_scan_qr_ready,
            cancel_callback=self.on_customer_id_scan_qr_cancel,
        )
        self.scr_manager().add_widget(self.scan_customer_id_screen)
        self.scr_manager().current = 'camera_scan_customer_id_screen'

    def on_customer_id_scan_qr_ready(self, *args):
        self.populated_customer_id_qr_scan = args[0].strip()
        if _Debug:
            print('on_customer_id_scan_qr_ready', self.populated_customer_id_qr_scan)
        self.scr_manager().current = 'sell_screen'
        self.scr_manager().remove_widget(self.scan_customer_id_screen)
        self.scan_customer_id_screen = None

    def on_customer_id_scan_qr_cancel(self, *args):
        self.scr_manager().current = 'sell_screen'
        self.scr_manager().remove_widget(self.scan_customer_id_screen)
        self.scan_customer_id_screen = None

    #------------------------------------------------------------------------------

    def on_receive_address_scan_qr_button_clicked(self, *args):
        self.scan_qr_screen = CameraScanQRScreen(
            name='camera_scan_qr_screen',
            scan_qr_callback=self.on_receive_address_scan_qr_ready,
            cancel_callback=self.on_receive_address_scan_qr_cancel,
        )
        self.scr_manager().add_widget(self.scan_qr_screen)
        self.scr_manager().current = 'camera_scan_qr_screen'

    def on_receive_address_scan_qr_ready(self, *args):
        self.populated_receive_address_qr_scan = args[0].strip()
        if _Debug:
            print('on_receive_address_scan_qr_ready', self.populated_receive_address_qr_scan)
        self.scr_manager().current = 'sell_screen'
        self.scr_manager().remove_widget(self.scan_qr_screen)
        self.scan_qr_screen = None

    def on_receive_address_scan_qr_cancel(self, *args):
        if _Debug:
            print('on_receive_address_scan_qr_cancel', args)
        self.scr_manager().current = 'sell_screen'
        self.scr_manager().remove_widget(self.scan_qr_screen)
        self.scan_qr_screen = None

    #------------------------------------------------------------------------------

    def on_clear_button_clicked(self, *args):
        self.clean_input_fields()
        self.populate_btc_usd_price()

    def on_coinmarketcap_response(self, request, response):
        if response:
            try:
                btc_usd_price = float(response['data'][0]['quote']['USD']['price'])
            except:
                import traceback
                traceback.print_exc()
                btc_usd_price = None
            if btc_usd_price is not None:
                self.ids.btc_price_input.text = '%.2f' % btc_usd_price

    #------------------------------------------------------------------------------

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
        self.populate_btc_amount_from_usd_amount()

    def on_btc_amount_input_changed_earlier(self, *args):
        self.populate_usd_amount_task = None
        if not self.ids.btc_amount_input.focused:
            return
        self.populate_usd_amount_from_btc_amount()

    #------------------------------------------------------------------------------

    def on_start_transaction_button_clicked(self):
        if not self.selected_customer_info:
            msg = 'Please select a customer first, click "Select customer" button.'
            dialogs.show_one_button_dialog(
                title='Need to select a cusomer',
                message=msg,
            )
            return
        bought, sold = local_storage.calculate_customer_transactions_this_month(self.selected_customer_id)
        if _Debug:
            print('sold: %r   bought: %r' % (sold, bought, ))
        limit_transactions = float(self.selected_customer_info.get('limit_transactions', '0') or '0')
        if limit_transactions:
            usd_amount = float(self.ids.usd_amount_input.text)
            if bought + usd_amount > limit_transactions:
                msg = 'Customer {} {} is only authorized for ${} per month.\n'.format(
                    self.ids.person_first_name_input.text,
                    self.ids.person_last_name_input.text,
                    limit_transactions,
                )
                msg += 'This month, the customer bought BTC for a total of ${}.'.format(bought)
                dialogs.show_one_button_dialog(
                    title='Transactions amount limit exceeded',
                    message=msg,
                )
                return
        cur_settings = local_storage.read_settings()
        t_now = datetime.datetime.now()
        btc_usd_commission_percent = float(cur_settings.get('btc_usd_commission_percent', '0.0'))
        btc_price_current = float(self.ids.btc_price_input.text)
        factor = (100.0 + btc_usd_commission_percent) / 100.0
        contract_btc_price = str(round(btc_price_current * factor, 2))
        transaction_details = {}
        transaction_details.update(dict(
            contract_type='sales',
            lightning=self.ids.receive_address_input.text.lower().startswith('lnbc'),
            usd_amount=self.ids.usd_amount_input.text,
            world_btc_price=self.ids.btc_price_input.text,
            btc_price=contract_btc_price,
            btc_amount=btc_util.clean_btc_amount(self.ids.btc_amount_input.text),
            fee_percent=str(float(cur_settings.get('btc_usd_commission_percent', '0.0'))),
            date=t_now.strftime("%b %d %Y"),
            time=t_now.strftime("%I:%M %p"),
            seller=dict(
                customer_id=None,
                first_name=cur_settings.get('business_owner_first_name', ''),
                last_name=cur_settings.get('business_owner_last_name', ''),
                address=cur_settings.get('business_address', ''),
                email=cur_settings.get('business_email', ''),
                phone=cur_settings.get('business_phone', ''),
                btc_address=(cur_settings.get('receiving_btc_address_list', ['', ]) or ['', ])[0],
            ),
            buyer=dict(
                customer_id=self.selected_customer_id,
                first_name=self.ids.person_first_name_input.text,
                last_name=self.ids.person_last_name_input.text,
                address=self.ids.person_address_input.text,
                email=self.ids.person_email_input.text,
                phone=self.ids.person_phone_input.text,
                btc_address=self.ids.receive_address_input.text,
            ),
            company_name=cur_settings.get('business_company_name', ''),
            blockchain_status='unconfirmed',
            confirmed_time=None,
        ))
        new_transaction_details = local_storage.create_new_transaction(transaction_details)
        local_storage.write_transaction(new_transaction_details['transaction_id'], new_transaction_details)
        self.clean_input_fields()
        self.scr('one_transaction_screen').transaction_id = new_transaction_details['transaction_id']
        self.scr_manager().current = 'one_transaction_screen'
