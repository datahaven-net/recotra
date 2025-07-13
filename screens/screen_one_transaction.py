import os
import datetime

#------------------------------------------------------------------------------

from kivy.metrics import dp

#------------------------------------------------------------------------------

from components.screen import AppScreen
from components import dialogs

from lib import render_pdf
from lib import system
from lib import btc_util

from storage import local_storage

#------------------------------------------------------------------------------

_Debug = False

#------------------------------------------------------------------------------

kv = """
<TransactionFieldLabel@RightAlignLabel>:
    size_hint_x: None
    width: dp(200)
    valign: 'middle'
    color: (.5,.5,.5,1)


<TransactionFieldHeader@TransactionFieldLabel>:
    color: (0,0,0,1)


<TransactionFieldValue@LeftAlignLabel>:
    size_hint_x: None
    width: dp(515)
    valign: 'middle'


<OneTransactionScreen>:

    BoxLayout:
        orientation: 'vertical'
        size_hint: 1, 1

        ScrollView:
            bar_width: dp(15)
            bar_color: .2,.5,.8,1
            bar_inactive_color: .1,.4,.7,1
            effect_cls: "ScrollEffect"
            scroll_type: ['bars']

            GridLayout:
                size_hint_x: None
                size_hint_y: None
                width: self.minimum_width
                height: self.minimum_height
                cols: 2
                padding: dp(10)
                spacing: dp(2)
                row_force_default: False
                row_default_height: dp(22)

                TransactionFieldHeader:
                    id: contract_type_input
                    size_hint_y: None
                    height: dp(80)
                    valign: 'bottom'
                    text: ''
                Widget:
                    size: 1, 1

                Widget:
                    size: 1, dp(10)
                Widget:
                    size: 1, dp(10)

                TransactionFieldHeader:
                    text: "[size=20]Seller[/size]"
                Widget:
                    size: 1, 1
                TransactionFieldLabel:
                    text: "first name:"
                TransactionFieldValue:
                    id: seller_first_name_input
                    text: ''
                TransactionFieldLabel:
                    text: "last name:"
                TransactionFieldValue:
                    id: seller_last_name_input
                    text: ''
                TransactionFieldLabel:
                    text: "phone:"
                TransactionFieldValue:
                    id: seller_phone_input
                    text: ''
                TransactionFieldLabel:
                    text: "e-mail:"
                TransactionFieldValue:
                    id: seller_email_input
                    text: ''
                TransactionFieldLabel:
                    text: "street address:"
                TransactionFieldValue:
                    id: seller_address_input
                    text: ''

                TransactionFieldHeader:
                    text: "[size=20]Buyer[/size]"
                Widget:
                    size: 1, 1
                TransactionFieldLabel:
                    text: "first name:"
                TransactionFieldValue:
                    id: buyer_first_name_input
                    text: ''
                TransactionFieldLabel:
                    text: "last name:"
                TransactionFieldValue:
                    id: buyer_last_name_input
                    text: ''
                TransactionFieldLabel:
                    text: "phone:"
                TransactionFieldValue:
                    id: buyer_phone_input
                    text: ''
                TransactionFieldLabel:
                    text: "e-mail:"
                TransactionFieldValue:
                    id: buyer_email_input
                    text: ''
                TransactionFieldLabel:
                    text: "street address:"
                TransactionFieldValue:
                    id: buyer_address_input
                    text: ''

                TransactionFieldHeader:
                    text: "[size=20]Contract details[/size]"
                Widget:
                    size: 1, 1

                TransactionFieldLabel:
                    text: "amount (US $):"
                TransactionFieldValue:
                    id: usd_amount_input
                    text: ''
                TransactionFieldLabel:
                    text: "BTC price (US $ / BTC):"
                TransactionFieldValue:
                    id: btc_price_input
                    text: ''
                TransactionFieldLabel:
                    text: "coinmarketcap.com price:"
                TransactionFieldValue:
                    id: world_btc_price_input
                    text: ''
                TransactionFieldLabel:
                    text: "BTC Amount:"
                TransactionFieldValue:
                    id: btc_amount_input
                    text: ''
                TransactionFieldLabel:
                    text: "started:"
                TransactionFieldValue:
                    id: started_date_time_input
                    text: ''

                TransactionFieldLabel:
                    text: "spending BitCoin address:"
                TransactionFieldValue:
                    id: spending_btc_address_input
                    text: ''
                TransactionFieldLabel:
                    text: "receiving BitCoin address:"
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint: None, None
                    width: dp(545)
                    height: self.minimum_height
                    CloseButton:
                        size_hint: None, None
                        width: dp(20)
                        height: dp(20)
                        text: fa_icon('edit')
                        font_size: sp(10)
                        on_release: root.on_receiving_btc_address_change_button_clicked()
                    TransactionFieldValue:
                        id: receiving_btc_address_input
                        text: ''

                TransactionFieldLabel:
                    text: "blockchain status:"
                TransactionFieldValue:
                    id: blockchain_status_input
                    text: ''

                TransactionFieldLabel:
                    text: "payment type:"
                TransactionFieldValue:
                    id: payment_type_input
                    text: ''
                TransactionFieldLabel:
                    text: "Bank account info:"
                TransactionFieldValue:
                    id: bank_info_input
                    text: ''

                TransactionFieldHeader:
                    text: "[size=20]Attachments[/size]"
                Widget:
                    size: 1, 1

                TransactionFieldLabel:
                    text: ''
                TransactionFieldValue:
                    id: attachments_input
                    text_size: self.width, None
                    size_hint: 1, None
                    height: self.texture_size[1]
                    text: ''

        LeftAlignLabel:
            id: verify_status_label
            size_hint: 1, None
            height: dp(20)
            text: ''

        BoxLayout:
            orientation: 'horizontal'
            size_hint: None, None
            height: self.minimum_height
            padding: dp(10)
            spacing: dp(2)

            RoundedButton:
                text: 'print contract'
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_pdf_file_button_clicked()

            Widget:
                size_hint: None, 1
                width: dp(20)

            RoundedButton:
                text: 'print attachments'
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_attachments_button_clicked()

            Widget:
                size_hint: None, 1
                width: dp(20)

            RoundedButton:
                id: verify_button
                text: 'verify on blockchain'
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_verify_button_clicked()

            Widget:
                size_hint: None, 1
                width: dp(20)

            RoundedButton:
                id: explore_button
                text: 'explore on blockchain'
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_explore_button_clicked()

            Widget:
                size_hint: None, 1
                width: dp(20)

            RoundedButton:
                id: confirm_button
                text: 'mark as confirmed'
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_confirm_button_clicked()

"""

#------------------------------------------------------------------------------

class OneTransactionScreen(AppScreen):

    transaction_id = None

    def populate_fields(self, tran_details):
        self.ids.contract_type_input.text = '[size=20]BTC%s\n%s contract\n#%s[/size]' % (
            ' Lightning' if tran_details.get('lightning') else '',
            ('purchase' if tran_details['contract_type'] == 'purchase' else 'sales'),
            tran_details['transaction_id'],
        )

        self.ids.seller_first_name_input.text = tran_details['seller']['first_name'] or ''
        self.ids.seller_last_name_input.text = tran_details['seller']['last_name'] or ''
        self.ids.seller_phone_input.text = tran_details['seller']['phone'] or ''
        self.ids.seller_email_input.text = tran_details['seller']['email'] or ''
        self.ids.seller_address_input.text = tran_details['seller']['address'] or ''

        self.ids.buyer_first_name_input.text = tran_details['buyer']['first_name'] or ''
        self.ids.buyer_last_name_input.text = tran_details['buyer']['last_name'] or ''
        self.ids.buyer_phone_input.text = tran_details['buyer']['phone'] or ''
        self.ids.buyer_email_input.text = tran_details['buyer']['email'] or ''
        self.ids.buyer_address_input.text = tran_details['buyer']['address'] or ''

        self.ids.usd_amount_input.text = tran_details.get('usd_amount') or ''
        self.ids.btc_price_input.text = tran_details.get('btc_price') or ''
        self.ids.world_btc_price_input.text = tran_details.get('world_btc_price') or ''
        self.ids.btc_amount_input.text = tran_details.get('btc_amount') or ''
        if self.ids.btc_amount_input.text:
            self.ids.btc_amount_input.text = '{} BTC = {} mBTC'.format(
                self.ids.btc_amount_input.text, str(float(self.ids.btc_amount_input.text) * 1000.0))

        if tran_details['contract_type'] == 'purchase':
            self.ids.receiving_btc_address_input.text = tran_details['buyer']['btc_address'] or ''
            self.ids.spending_btc_address_input.text = ''  # tran_details['seller']['btc_address'] or ''
        else:
            self.ids.receiving_btc_address_input.text = tran_details['buyer']['btc_address'] or ''
            self.ids.spending_btc_address_input.text = ''  # tran_details['seller']['btc_address'] or ''

        if tran_details.get('lightning'):
            self.ids.receiving_btc_address_input.size_hint_y = None
            self.ids.receiving_btc_address_input.height = dp(80)
        else:
            self.ids.receiving_btc_address_input.size_hint_y = None
            self.ids.receiving_btc_address_input.height = dp(20)

        self.ids.blockchain_status_input.text = '[color={}][{}][/color]'.format(
            '#a0a060' if tran_details.get('blockchain_status') != 'confirmed' else '#60b060',
            tran_details.get('blockchain_status', 'unconfirmed'),
        )
        self.ids.started_date_time_input.text = '{} at {}'.format(tran_details['date'] or '', tran_details['time'] or '')
        self.ids.verify_button.disabled = tran_details.get('blockchain_status', 'unconfirmed') == 'confirmed'
        self.ids.payment_type_input.text = (tran_details.get('payment_type') or 'cash').replace('on-line', 'bank transfer')
        self.ids.bank_info_input.text = tran_details['seller'].get('bank_info') or '(not provided)'

        attachments_dir_path = local_storage.transaction_attachments_dir_path(self.transaction_id)
        attachments_text_list = []
        if os.path.isdir(attachments_dir_path):
            for attachment in os.listdir(attachments_dir_path):
                attachments_text_list.append(attachment)
        self.ids.attachments_input.text = ', '.join(attachments_text_list)

    def on_enter(self, *args):
        self.ids.verify_status_label.text = ''
        if self.transaction_id is None:
            return
        tran_details = local_storage.read_transaction(self.transaction_id)
        self.populate_fields(tran_details)

    def on_pdf_file_button_clicked(self):
        cur_settings = local_storage.read_settings()
        transaction_details = local_storage.read_transaction(self.transaction_id)
        if transaction_details:
            pdf_contract = render_pdf.build_pdf_contract(
                transaction_details=transaction_details,
                disclosure_statement=cur_settings.get('disclosure_statement') or '',
                pdf_filepath=os.path.join(local_storage.contracts_dir(), 'transaction_{}.pdf'.format(self.transaction_id)),
            )
            if _Debug:
                print('pdf_contract:', pdf_contract['filename'])
            system.open_path_in_os(pdf_contract['filename'])

    def on_attachments_button_clicked(self):
        attachments_dir_path = local_storage.transaction_attachments_dir_path(self.transaction_id)
        if os.path.isdir(attachments_dir_path):
            for attachment in os.listdir(attachments_dir_path):
                system.open_system_explorer(os.path.join(attachments_dir_path, attachment), as_folder=True)

    def on_confirm_button_clicked(self):
        transaction_details = local_storage.read_transaction(self.transaction_id)
        if transaction_details.get('blockchain_status') == 'confirmed':
            return
        if transaction_details.get('void'):
            return
        st = ''
        if transaction_details.get('lightning'):
            transaction_details['blockchain_status'] = 'confirmed'
            transaction_details['confirmed_time'] = datetime.datetime.now().strftime("%b %d %Y %I:%M %p")
            st = '[color=#70a070]confirmed lightning transaction of %s BTC for address %s...[/color]' % (
                transaction_details['btc_amount'], transaction_details['buyer']['btc_address'][:40])
        else:
            self.ids.verify_button.disabled = True
            st = '[color=#a07070]manually marked transaction of %s BTC for address %s as "confirmed"[/color]' % (
                transaction_details['btc_amount'], transaction_details['buyer']['btc_address'])
            transaction_details['blockchain_status'] = 'confirmed'
            transaction_details['blockchain_tx_info'] = None
            transaction_details['confirmed_time'] = datetime.datetime.now().strftime("%b %d %Y %I:%M %p")
        local_storage.write_transaction(transaction_details['transaction_id'], transaction_details)
        self.ids.verify_status_label.text = st
        self.populate_fields(transaction_details)

    def on_verify_button_clicked(self):
        transaction_details = local_storage.read_transaction(self.transaction_id)
        if transaction_details.get('blockchain_status') == 'confirmed':
            return
        if transaction_details.get('void'):
            return
        cur_settings = local_storage.read_settings()
        st = ''
        if transaction_details.get('lightning'):
            transaction_details['blockchain_status'] = 'confirmed'
            transaction_details['confirmed_time'] = datetime.datetime.now().strftime("%b %d %Y %I:%M %p")
            st = '[color=#70a070]automatically confirm lightning transaction of %s BTC for address %s...[/color]' % (
                transaction_details['btc_amount'], transaction_details['buyer']['btc_address'][:40])
            local_storage.write_transaction(transaction_details['transaction_id'], transaction_details)
        else:
            self.ids.verify_button.disabled = True
            self.ids.verify_status_label.text = '[color=#505050]requesting transactions from btc.com ...[/color]'
            matching_transactions = btc_util.verify_contract(
                contract_details=transaction_details,
                price_precision_fixed_amount=float(cur_settings.get('price_precision_fixed_amount', '0.0')),
                price_precision_matching_percent=float(cur_settings.get('price_precision_matching_percent', '0.0')),
                time_matching_seconds_before=float(cur_settings.get('time_matching_seconds_before', '0.0')),
                time_matching_seconds_after=float(cur_settings.get('time_matching_seconds_after', '0.0')),
            )
            self.ids.verify_button.disabled = False
            if len(matching_transactions) == 0:
                st = '[color=#505050]did not found any matching transactions for BTC address %s[/color]' % transaction_details['buyer']['btc_address']
            elif len(matching_transactions) > 1:
                st = '[color=#F05050]found multiple matching transactions for BTC address %s[/color]' % transaction_details['buyer']['btc_address']
            else:
                st = '[color=#70a070]found corresponding transaction of %s BTC for address %s[/color]' % (
                    transaction_details['btc_amount'], transaction_details['buyer']['btc_address'])
                transaction_details['blockchain_status'] = 'confirmed'
                transaction_details['blockchain_tx_info'] = matching_transactions[0]
                transaction_details['confirmed_time'] = datetime.datetime.now().strftime("%b %d %Y %I:%M %p")
                local_storage.write_transaction(transaction_details['transaction_id'], transaction_details)
        self.ids.verify_status_label.text = st
        self.populate_fields(transaction_details)

    def on_explore_button_clicked(self):
        transaction_details = local_storage.read_transaction(self.transaction_id)
        if not transaction_details.get('lightning'):
            system.open_webbrowser(
                url='https://www.blockchain.com/btc/address/' + transaction_details.get('buyer', {}).get('btc_address', ''),
            )

    def on_receiving_btc_address_change_button_clicked(self):
        transaction_details = local_storage.read_transaction(self.transaction_id)
        if transaction_details.get('blockchain_status') == 'confirmed':
            return
        dlg = dialogs.BTCAddressDialog(
            btc_address=self.ids.receiving_btc_address_input.text,
            callback=self.on_receiving_btc_address_changed,
        )
        dlg.open()

    def on_receiving_btc_address_changed(self, txt):
        self.ids.receiving_btc_address_input.text = txt
        transaction_details = local_storage.read_transaction(self.transaction_id)
        transaction_details['buyer']['btc_address'] = txt
        transaction_details['lightning'] = txt.lower().startswith('lnbc'),
        local_storage.write_transaction(transaction_details['transaction_id'], transaction_details)
