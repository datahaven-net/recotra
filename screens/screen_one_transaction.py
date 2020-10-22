import os

#------------------------------------------------------------------------------

from components.screen import AppScreen

from lib import render_pdf
from lib import system

from storage import local_storage

#------------------------------------------------------------------------------

kv = """
<OneTransactionScreen>:

    BoxLayout:
        orientation: 'vertical'
        size_hint: 1, 1

        ScrollView:
            bar_width: 15
            bar_color: .2,.5,.8,1
            bar_inactive_color: .1,.4,.7,1
            effect_cls: "ScrollEffect"
            scroll_type: ['bars']

            GridLayout:
                size_hint_y: None
                height: self.minimum_height
                cols: 2
                padding: 10
                spacing: 2
                row_force_default: True
                row_default_height: 40

                RightAlignLabel:
                    id: contract_type_input
                    text: ""
                Widget:
                    size: 1, 1

                RightAlignLabel:
                    text: "[size=20]Seller:[/size]"
                Widget:
                    size: 1, 1
                RightAlignLabel:
                    text: "first name:"
                LeftAlignLabel:
                    id: seller_first_name_input
                    text: ""
                RightAlignLabel:
                    text: "last name:"
                LeftAlignLabel:
                    id: seller_last_name_input
                    text: ""
                RightAlignLabel:
                    text: "phone:"
                LeftAlignLabel:
                    id: seller_phone_input
                    text: ""
                RightAlignLabel:
                    text: "e-mail:"
                LeftAlignLabel:
                    id: seller_email_input
                    text: ""
                RightAlignLabel:
                    text: "street address:"
                LeftAlignLabel:
                    id: seller_address_input
                    text: ""

                RightAlignLabel:
                    text: "[size=20]Buyer:[/size]"
                Widget:
                    size: 1, 1
                RightAlignLabel:
                    text: "first name:"
                LeftAlignLabel:
                    id: buyer_first_name_input
                    text: ""
                RightAlignLabel:
                    text: "last name:"
                LeftAlignLabel:
                    id: buyer_last_name_input
                    text: ""
                RightAlignLabel:
                    text: "phone:"
                LeftAlignLabel:
                    id: buyer_phone_input
                    text: ""
                RightAlignLabel:
                    text: "e-mail:"
                LeftAlignLabel:
                    id: buyer_email_input
                    text: ""
                RightAlignLabel:
                    text: "street address:"
                LeftAlignLabel:
                    id: buyer_address_input
                    text: ""

                RightAlignLabel:
                    text: "[size=20]Contract details:[/size]"
                Widget:
                    size: 1, 1

                RightAlignLabel:
                    text: "amount (US $):"
                LeftAlignLabel:
                    id: usd_amount_input
                    text: ""
                RightAlignLabel:
                    text: "BTC price (US $ / BTC):"
                LeftAlignLabel:
                    id: btc_price_input
                    text: ""
                RightAlignLabel:
                    text: "BTC Amount:"
                LeftAlignLabel:
                    id: btc_amount_input
                    text: ""
                RightAlignLabel:
                    text: "started:"
                LeftAlignLabel:
                    id: started_date_time_input
                    text: ""

                RightAlignLabel:
                    text: "spending BitCoin address:"
                LeftAlignLabel:
                    id: spending_btc_address_input
                    text: ""
                RightAlignLabel:
                    text: "receiving BitCoin address:"
                LeftAlignLabel:
                    id: receiving_btc_address_input
                    text: ""

                RightAlignLabel:
                    text: "blockchain status:"
                LeftAlignLabel:
                    id: blockchain_status_input
                    text: ""

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, None
            padding: 10
            spacing: 2

            RoundedButton:
                text: 'print contract'
                width: 160
                size_hint_x: None
                on_release: root.on_pdf_file_button_clicked()
"""

#------------------------------------------------------------------------------

class OneTransactionScreen(AppScreen):

    transaction_id = None

    def populate_fields(self, tran_details):
        self.ids.contract_type_input.text = '[size=30]BTC %s Contract #%s[/size]' % (
            ('Purchase' if tran_details['contract_type'] == 'purchase' else 'Sales'),
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

        self.ids.usd_amount_input.text = tran_details['usd_amount'] or ''
        self.ids.btc_price_input.text = tran_details['btc_price'] or ''
        self.ids.btc_amount_input.text = tran_details['btc_amount'] or ''

        if tran_details['contract_type'] == 'purchase':
            self.ids.receiving_btc_address_input.text = tran_details['buyer']['btc_address'] or ''
            self.ids.spending_btc_address_input.text = ''  # tran_details['seller']['btc_address'] or ''
        else:
            self.ids.receiving_btc_address_input.text = tran_details['buyer']['btc_address'] or ''
            self.ids.spending_btc_address_input.text = ''  # tran_details['seller']['btc_address'] or ''

        self.ids.blockchain_status_input.text = '[unconfirmed]'
        self.ids.started_date_time_input.text = '{} at {}'.format(tran_details['date'] or '', tran_details['time'] or '')

    def on_pre_enter(self, *args):
        if self.transaction_id is None:
            return
        tran_details = local_storage.read_transaction(self.transaction_id)
        self.populate_fields(tran_details)

    def on_pdf_file_button_clicked(self):
        transaction_details = local_storage.read_transaction(self.transaction_id)
        if transaction_details:
            buy_contract = render_pdf.build_pdf_contract(
                transaction_details=transaction_details,
                pdf_filepath=os.path.join(local_storage.contracts_dir(), 'transaction_{}.pdf'.format(self.transaction_id)),
            )
            system.open_system_explorer(buy_contract['filename'])
