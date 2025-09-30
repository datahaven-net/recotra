import os
import datetime
import tempfile
import shutil

#------------------------------------------------------------------------------

from kivy.clock import Clock
from kivy.clock import mainthread

#------------------------------------------------------------------------------

from lib import coinmarketcap_client
from lib import btc_util
from lib import system

from components.screen import AppScreen
from components import dialogs

from storage import local_storage

from screens.screen_camera_scan_qr import CameraScanQRScreen

#------------------------------------------------------------------------------

_Debug = False

#------------------------------------------------------------------------------

kv = """
<BuyFieldLabel@RightAlignLabel>:
    size_hint_x: None
    width: dp(190)
    valign: 'middle'


<BuyFieldInput@TextInput>:
    size_hint_x: None
    size_hint_y: None
    width: dp(510)
    height: self.minimum_height
    multiline: False
    write_tab: False

<BuyScreen>:

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
                id: attach_file_button
                text: "attach a file"
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_attach_file_button_clicked()

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
                text: "Customer selling BTC to Bitcoin.ai"

            GridLayout:
                size_hint_x: None
                size_hint_y: None
                width: self.minimum_width
                height: self.minimum_height
                cols: 2
                padding: dp(10)
                spacing: dp(10)

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
                    on_text: root.on_usd_amount_input_changed(self.text)

                BuyFieldLabel:
                    text: "BTC price (US $ / BTC):"
                BuyFieldInput:
                    id: btc_price_input
                    text: ""

                BuyFieldLabel:
                    text: "BTC amount:"
                BuyFieldInput:
                    id: btc_amount_input
                    text: ""
                    on_text: root.on_btc_amount_input_changed(self.text)

                BuyFieldLabel:
                    text: "receiving BitCoin address:"
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: self.minimum_height
                    BuyFieldInput:
                        id: receive_address_input
                        text: ""
                    RoundedButton:
                        size_hint: None, 1
                        width: self.texture_size[0] + dp(16)
                        text: fa_icon('camera')
                        on_release: root.on_receive_address_scan_qr_button_clicked()

                BuyFieldLabel:
                    text: ""
                CompactSpinner:
                    id: select_contract_type_button
                    width: dp(110)
                    text: 'contract type'
                    color: (1,0,0,1)
                    values: 'CASH', 'ON-LINE'
                    on_text: root.on_select_contract_type_button_clicked()

                BuyFieldLabel:
                    text: "Bank account info:"
                BuyFieldInput:
                    id: bank_info_input
                    text: ""
                    disabled: True

"""

#------------------------------------------------------------------------------

class BuyScreen(AppScreen):

    selected_customer_id = None
    selected_customer_info = None
    populate_usd_amount_task = None
    populate_btc_amount_task = None
    populated_receive_address_qr_scan = None
    populated_customer_id_qr_scan = None

    def __init__(self, **kw):
        super(BuyScreen, self).__init__(**kw)
        self.attachments = []

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
        self.ids.btc_amount_input.text = '0.0'
        self.ids.receive_address_input.text = ''
        self.ids.select_contract_type_button.text = 'contract type'
        self.ids.select_contract_type_button.color = (1,0,0,1)
        self.ids.bank_info_input.text = ''
        self.attachments = []

    def populate_next_btc_address(self):
        if self.ids.receive_address_input.text:
            return
        cur_settings = local_storage.read_settings()
        recent_btc_address = cur_settings.get('recent_btc_address') or ''
        receiving_btc_address_list = cur_settings.get('receiving_btc_address_list', [])
        if receiving_btc_address_list:
            recent_pos = -1
            if recent_btc_address and recent_btc_address in receiving_btc_address_list:
                recent_pos = receiving_btc_address_list.index(recent_btc_address)
            recent_pos += 1
            if recent_pos >= len(receiving_btc_address_list):
                recent_pos = 0
            self.ids.receive_address_input.text = receiving_btc_address_list[recent_pos].strip()
        if not self.ids.receive_address_input.text:
            self.ids.receive_address_input.text = recent_btc_address

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
            self.populate_next_btc_address()
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
        self.scr_manager().current = 'buy_screen'

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
        self.scr_manager().current = 'buy_screen'
        self.scr_manager().remove_widget(self.scan_customer_id_screen)
        self.scan_customer_id_screen = None

    def on_customer_id_scan_qr_cancel(self, *args):
        self.scr_manager().current = 'buy_screen'
        self.scr_manager().remove_widget(self.scan_customer_id_screen)
        self.scan_customer_id_screen = None

    #------------------------------------------------------------------------------

    def on_receive_address_scan_qr_button_clicked(self, *args):
        self.scan_qr_screen = CameraScanQRScreen(
            name='camera_scan_qr_screen',
            scan_qr_callback=self.on_buy_receive_address_scan_qr_ready,
            cancel_callback=self.on_buy_receive_address_scan_qr_cancel,
        )
        self.scr_manager().add_widget(self.scan_qr_screen)
        self.scr_manager().current = 'camera_scan_qr_screen'

    def on_buy_receive_address_scan_qr_ready(self, *args):
        self.populated_receive_address_qr_scan = args[0].strip()
        if _Debug:
            print('on_buy_receive_address_scan_qr_ready', self.populated_receive_address_qr_scan)
        self.scr_manager().current = 'buy_screen'
        self.scr_manager().remove_widget(self.scan_qr_screen)
        self.scan_qr_screen = None

    def on_buy_receive_address_scan_qr_cancel(self, *args):
        self.scr_manager().current = 'buy_screen'
        self.scr_manager().remove_widget(self.scan_qr_screen)
        self.scan_qr_screen = None

    #------------------------------------------------------------------------------

    def on_clear_button_clicked(self, *args):
        self.clean_input_fields()
        self.populate_btc_usd_price()

    def on_coinmarketcap_response(self, request, response):
        if _Debug:
            print('on_coinmarketcap_response', response)
        if response:
            try:
                btc_usd_price = float(response['data'][0]['quote']['USD']['price'])
            except:
                btc_usd_price = None
            if btc_usd_price is not None:
                self.ids.btc_price_input.text = '%.2f' % btc_usd_price

    #------------------------------------------------------------------------------

    def on_usd_amount_input_changed(self, new_text):
        if not new_text:
            return
        if self.populate_btc_amount_task:
            Clock.unschedule(self.populate_btc_amount_task)
            self.populate_btc_amount_task = Clock.schedule_once(self.on_usd_amount_input_changed_earlier, 0.1)
        else:
            self.populate_btc_amount_task = Clock.schedule_once(self.on_usd_amount_input_changed_earlier, 0.1)

    def on_btc_amount_input_changed(self, new_text):
        if not new_text:
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
            usd_btc_commission_percent = float(cur_settings.get('usd_btc_commission_percent', '0.0'))
            btc_price_current = float(self.ids.btc_price_input.text)
            rate_for_this_contract = btc_price_current * (1.0 + usd_btc_commission_percent / 100.0)
        except:
            return
        if btc_price_current:
            t = ('%.6f' % round(usd_amount_current / rate_for_this_contract, 6)).rstrip('0')
            if t.endswith('.'):
                t += '0'
            self.ids.btc_amount_input.text = t

    def on_btc_amount_input_changed_earlier(self, *args):
        self.populate_usd_amount_task = None
        if not self.ids.btc_amount_input.focused:
            return
        cur_settings = local_storage.read_settings()
        try:
            btc_amount_current = float(btc_util.clean_btc_amount(self.ids.btc_amount_input.text))
            usd_btc_commission_percent = float(cur_settings.get('usd_btc_commission_percent', '0.0'))
            btc_price_current = float(self.ids.btc_price_input.text)
            rate_for_this_contract = btc_price_current * (1.0 + usd_btc_commission_percent / 100.0)
        except:
            return
        self.ids.usd_amount_input.text = '%.2f' % round(btc_amount_current * rate_for_this_contract, 2)

    #------------------------------------------------------------------------------

    @mainthread
    def on_attach_file_button_clicked(self, *args):
        if _Debug:
            print('BuyScreen.on_attach_file_button_clicked', args)
        if system.is_osx():
            from lib import filechooser_macosx
            fc = filechooser_macosx.MacFileChooser(
                title="Upload a file",
                preview=True,
                show_hidden=False,
                on_selection=self.on_upload_file_selected,
            )
            fc.run()
        else:
            from plyer import filechooser  # @UnresolvedImport
            if system.is_windows():
                self._latest_cwd = os.getcwd()
            filechooser.open_file(
                title="Upload a file",
                preview=True,
                show_hidden=False,
                on_selection=self.on_upload_file_selected,
            )

    def on_upload_file_selected(self, *args, **kwargs):
        if _Debug:
            print('BuyScreen.on_upload_file_selected', args, kwargs)
        if system.is_windows():
            try:
                os.chdir(self._latest_cwd)
            except:
                pass
        file_path = args[0][0]
        file_name = os.path.basename(file_path)
        if not os.path.isfile(file_path):
            if _Debug:
                print('BuyScreen.on_upload_file_selected file do not exist', file_path)
            return
        attachment_temp_file_path = tempfile.mktemp(
            suffix='_' + file_name,
            prefix='attachment_',
            dir=local_storage.temp_dir(),
        )
        try:
            shutil.copy(file_path, attachment_temp_file_path)
        except Exception as exc:
            if _Debug:
                print('BuyScreen.on_upload_file_selected :', exc)
            return
        self.attachments.append(attachment_temp_file_path)

    #------------------------------------------------------------------------------

    def on_select_contract_type_button_clicked(self, *args, **kwargs):
        if _Debug:
            print('BuyScreen.on_select_contract_type_button_clicked', self.ids.select_contract_type_button.text)
        if self.ids.select_contract_type_button.text in ('CASH', 'ON-LINE'):
            self.ids.select_contract_type_button.color = (0,0,0,1)
            if self.ids.select_contract_type_button.text == 'ON-LINE':
                self.ids.bank_info_input.disabled = False
            else:
                self.ids.bank_info_input.disabled = True
                self.ids.bank_info_input.text = ''

    #------------------------------------------------------------------------------

    def on_start_transaction_button_clicked(self):
        cur_settings = local_storage.read_settings()
        if self.ids.select_contract_type_button.text not in ('CASH', 'ON-LINE'):
            dialogs.show_one_button_dialog(
                title='Need to select payment type',
                message='Please select a payment type for the new contract: CASH or ON-LINE.',
            )
            return
        if self.ids.select_contract_type_button.text == 'ON-LINE':
            if not self.ids.bank_info_input.text.strip():
                dialogs.show_one_button_dialog(
                    title='Need to provide customer Bank account info',
                    message='Please fill in Bank account information to start the contract.',
                )
                return
        if not self.selected_customer_info:
            dialogs.show_one_button_dialog(
                title='Need to select a cusomer',
                message='Please select a customer first, click "Select customer" button.',
            )
            return
        if self.selected_customer_info.get('is_blocked'):
            dialogs.show_one_button_dialog(
                title='Customer is currently flagged and restricted for any transactions.',
                message=self.selected_customer_info.get('text_notes') or 'No additional information was provided.',
            )
            return
        if not self.selected_customer_info.get('id_expire_date'):
            customer_info = local_storage.read_customer_info(self.selected_customer_id)
            if customer_info:
                self.selected_customer_info = customer_info
        if not self.selected_customer_info.get('id_expire_date'):
            dialogs.show_one_button_dialog(
                title='Must provide ID / Passport expiration date',
                message='Please update customer profile with actual ID / Passport expiration date.',
            )
            return
        try:
            id_expire_date = datetime.date(*map(int, self.selected_customer_info.get('id_expire_date').split('-')))
        except Exception as e:
            if _Debug:
                print('invalid id_expire_date %r: %r' % (e, self.selected_customer_info.get('id_expire_date'), ))
            dialogs.show_one_button_dialog(
                title='Invalid ID / Passport expiration date',
                message='Please update customer profile with currect ID / Passport expiration date.',
            )
            return
        if datetime.datetime.now().date() > id_expire_date:
            dialogs.show_one_button_dialog(
                title='Customer ID / Passport is expired',
                message='The ID / Passport of the client whose details are currently stored in the database has expired:\n\n%s' % self.selected_customer_info.get('id_expire_date'),
            )
            return
        bought, sold = local_storage.calculate_customer_transactions_this_month(self.selected_customer_id)
        if _Debug:
            print('sold: %r   bought: %r' % (sold, bought, ))
        usd_amount = float(self.ids.usd_amount_input.text)
        limit_transactions = float(self.selected_customer_info.get('limit_transactions', '0') or '0')
        if limit_transactions > 0:
            if sold + usd_amount > limit_transactions:
                msg = 'Customer {} {} is only authorized for ${} per month.\n'.format(
                    self.ids.person_first_name_input.text,
                    self.ids.person_last_name_input.text,
                    limit_transactions,
                )
                msg += 'This month, the customer sold BTC for a total of ${}.'.format(sold)
                dialogs.show_one_button_dialog(
                    title='Transactions amount limit exceeded',
                    message=msg,
                )
                return
        source_of_funds_limit = float(cur_settings.get('source_of_funds_limit', '5000'))
        if usd_amount >= source_of_funds_limit:
            if not self.attachments:
                dialogs.show_one_button_dialog(
                    title='Source of funds is required',
                    message='For contracts more than $%s customers must provide documents to prove their source of funds. Click "attach a file" button and select scanned document file location.' % int(source_of_funds_limit),
                )
                return
        t_now = datetime.datetime.now()
        usd_btc_commission_percent = float(cur_settings.get('usd_btc_commission_percent', '0.0'))
        btc_price_current = float(self.ids.btc_price_input.text)
        factor = (100.0 + usd_btc_commission_percent) / 100.0
        contract_btc_price = str(round(btc_price_current * factor, 2))
        is_lightning = self.ids.receive_address_input.text.lower().startswith('lnbc')
        transaction_details = {}
        transaction_details.update(dict(
            contract_type='purchase',
            payment_type=self.ids.select_contract_type_button.text.lower(),
            lightning=is_lightning,
            usd_amount=self.ids.usd_amount_input.text,
            world_btc_price=self.ids.btc_price_input.text,
            btc_price=contract_btc_price,
            btc_amount=btc_util.clean_btc_amount(self.ids.btc_amount_input.text),
            fee_percent=str(float(cur_settings.get('usd_btc_commission_percent', '0.0'))),
            date=t_now.strftime("%b %d %Y"),
            time=t_now.strftime("%I:%M %p"),
            seller=dict(
                customer_id=self.selected_customer_id,
                first_name=self.ids.person_first_name_input.text,
                last_name=self.ids.person_last_name_input.text,
                btc_address=self.ids.receive_address_input.text,
                address=self.ids.person_address_input.text,
                email=self.ids.person_email_input.text,
                phone=self.ids.person_phone_input.text,
                bank_info=self.ids.bank_info_input.text.strip() if self.ids.select_contract_type_button.text == 'ON-LINE' else '',
            ),
            buyer=dict(
                customer_id=None,
                first_name=cur_settings.get('business_owner_first_name', ''),
                last_name=cur_settings.get('business_owner_last_name', ''),
                address=cur_settings.get('business_address', ''),
                email=cur_settings.get('business_email', ''),
                phone=cur_settings.get('business_phone', ''),
                btc_address=self.ids.receive_address_input.text,
            ),
            company_name=cur_settings.get('business_company_name', ''),
            blockchain_status='unconfirmed',
            confirmed_time=None,
        ))
        new_transaction_details = local_storage.create_new_transaction(transaction_details)
        local_storage.write_transaction(new_transaction_details['transaction_id'], new_transaction_details)
        attachments_dir_path = local_storage.transaction_attachments_dir_path(new_transaction_details['transaction_id'])
        if not os.path.isdir(attachments_dir_path):
            os.mkdir(attachments_dir_path)
        for attachment in self.attachments:
            attachment_file_name = os.path.basename(attachment)
            destination_path = os.path.join(attachments_dir_path, attachment_file_name)
            try:
                os.rename(attachment, destination_path)
            except Exception as exc:
                if _Debug:
                    print('was not able to rename file %r to %r : %r' % (attachment, destination_path, exc))
        if not is_lightning:
            cur_settings['recent_btc_address'] = self.ids.receive_address_input.text
        local_storage.write_settings(cur_settings)
        self.clean_input_fields()
        self.scr('one_transaction_screen').transaction_id = new_transaction_details['transaction_id']
        self.scr_manager().current = 'one_transaction_screen'
