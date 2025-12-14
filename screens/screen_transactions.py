import os
import datetime

#------------------------------------------------------------------------------

from kivy.clock import Clock
from kivy.properties import ListProperty  # @UnresolvedImport

#------------------------------------------------------------------------------

from components import screen
from components import list_view

from storage import local_storage

from lib import system
from lib import render_pdf
from lib import render_csv
from lib import btc_util

#------------------------------------------------------------------------------

_Debug = False

#------------------------------------------------------------------------------

kv = """
<TransactionRecord>:

    canvas.before:
        Color:
            rgba: (.9, .9, 1, 1) if self.selected else (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size

    orientation: 'lr-tb'
    height: dp(70)
    size_hint_y: None
    tr_id: 'tr_id'
    tr_type: 'tr_type'
    buyer: 'buyer'
    seller: 'seller'
    from_to: 'from_to'
    blockchain_status: 'blockchain_status'
    amount_usd: 'amount_usd'
    amount_btc: 'amount_btc'
    price_btc: 'price_btc'
    date: 'date'
    void: 'void'

    Label:
        id: tr_id
        text: root.tr_id
        size_hint: None, 0.35
        width: dp(40)
        color: (0,0,0,.5) if root.void == '1' else (0,0,0,1)
    Label:
        id: seller
        text: '[color=#0000aa][ref=transaction_'+root.tr_id+']<'+root.seller+'>[/ref][/color]'
        markup: True
        bold: True
        size_hint: None, 0.35
        width: self.texture_size[0] + dp(5)
        color: (0,0,0,.5) if root.void == '1' else (0,0,0,1)
        on_ref_press: root.on_seller_text_ref_pressed(*args)
    Label:
        id: tr_type
        text: root.tr_type
        size_hint: None, 0.35
        width: self.texture_size[0] + dp(5)
        color: (0,0,0,.5) if root.void == '1' else (0,0,0,1)
    Label:
        id: amount_btc
        text: root.amount_btc
        markup: True
        size_hint: None, 0.35
        width: self.texture_size[0] + dp(5)
        color: (0,0,0,.5) if root.void == '1' else (0,0,0,1)
    Label:
        id: buyer
        text: '[color=#0000aa][ref=transaction_'+root.tr_id+']<'+root.buyer+'>[/ref][/color]'
        markup: True
        bold: True
        size_hint: None, 0.35
        width: self.texture_size[0] + dp(5)
        color: (0,0,0,.5) if root.void == '1' else (0,0,0,1)
        on_ref_press: root.on_buyer_text_ref_pressed(*args)
    Label:
        id: price_btc
        text: root.price_btc
        markup: True
        size_hint: None, 0.35
        width: self.texture_size[0] + dp(5)
        color: (0,0,0,.5) if root.void == '1' else (0,0,0,1)
    Label:
        id: amount_usd
        text: root.amount_usd
        markup: True
        size_hint: None, 0.35
        width: self.texture_size[0] + dp(5)
        color: (0,0,0,.5) if root.void == '1' else (0,0,0,1)
    Label:
        id: date
        text: root.date
        size_hint: None, 0.35
        width: self.texture_size[0] + dp(5)
        color: (0,0,0,.5) if root.void == '1' else (0,0,0,1)
    Label:
        id: from_to
        text: root.from_to
        size_hint: None, 0.35
        width: self.texture_size[0] + dp(5)
        color: (0,0,0,.5) if root.void == '1' else (0,0,0,1)
    Label:
        id: blockchain_status
        text: root.blockchain_status
        size_hint: None, 0.35
        width: self.texture_size[0] + dp(5)
        color: (0,0,0,.5) if root.void == '1' else (0,0,0,1)


<TransactionsView>:
    viewclass: 'TransactionRecord'

    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: False

<TransactionsScreen>:

    BoxLayout:
        orientation: 'vertical'

        TransactionsView:
            id: transactions_view
            size_hint: 1, 1

        BoxLayout:
            orientation: 'horizontal'
            size_hint: None, None
            height: self.minimum_height
            padding: dp(10)
            spacing: dp(2)

            RoundedButton:
                id: view_transaction_button
                text: 'view contract'
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                disabled: True
                on_release: root.on_view_transaction_button_clicked()

            RoundedButton:
                id: disable_transaction_button
                text: 'mark as "void"'
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                disabled: True
                on_release: root.on_disable_transaction_button_clicked()

            Widget:
                size_hint: None, 1
                width: dp(20)

            RoundedSpinner:
                id: select_month_button
                width: dp(84)
                text: '-'
                values: '-', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'

            RoundedSpinner:
                id: select_year_button
                width: dp(60)
                text: '-'
                values: '-', %s

            RoundedButton:
                text: 'PDF report'
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_print_pdf_transactions_button_clicked()

            RoundedButton:
                text: 'CSV report'
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_print_csv_transactions_button_clicked()

            Widget:
                size_hint: None, 1
                width: dp(20)

            RoundedButton:
                id: verify_contracts_button
                text: 'verify contracts'
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                on_release: root.on_verfy_transactions_button_clicked()

""" % ','.join(["'%s'" % y for y in range(datetime.date.today().year, datetime.date.today().year-5,-1)])

#------------------------------------------------------------------------------

class TransactionRecord(list_view.SelectableRecord):

    def on_seller_text_ref_pressed(self, *args):
        self.parent.parent.parent.parent.on_seller_text_ref_pressed(args[1])

    def on_buyer_text_ref_pressed(self, *args):
        self.parent.parent.parent.parent.on_buyer_text_ref_pressed(args[1])

#------------------------------------------------------------------------------

class TransactionsView(list_view.SelectableRecycleView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []

    def on_selection_applied(self, item, index, is_selected, prev_selected):
        self.parent.parent.ids.view_transaction_button.disabled = not is_selected
        if is_selected:
            if item.blockchain_status.count('unconfirmed') and item.void != '1':
                self.parent.parent.ids.disable_transaction_button.disabled = False
        else:
            self.parent.parent.ids.disable_transaction_button.disabled = True

    def populate(self, selected_customer_id=None):
        cur_settings = local_storage.read_settings()
        tr_list = []
        for t in local_storage.load_transactions_list():
            if not selected_customer_id:
                tr_list.append(t)
                continue
            if str(selected_customer_id) == str(t['buyer'].get('customer_id') or '') or str(selected_customer_id) == str(t['seller'].get('customer_id') or ''):
                tr_list.append(t)
        self.data = []
        for t in tr_list:
            seller_full_name = '[b]{} {}[/b]'.format(t['seller']['first_name'], t['seller']['last_name'])
            buyer_full_name = '[b]{} {}[/b]'.format(t['buyer']['first_name'], t['buyer']['last_name'])
            if t['contract_type'] == 'sales':
                seller_full_name = cur_settings.get('business_company_name') or seller_full_name
            else:
                buyer_full_name = cur_settings.get('business_company_name') or buyer_full_name
            self.data.append({
                'tr_id': str(t['transaction_id']),
                'tr_type': 'sold',
                'buyer': buyer_full_name,
                'buyer_id': t['buyer'].get('customer_id') or '',
                'amount_btc': '[b]{}[/b] BTC to'.format(t['btc_amount']),
                'seller': seller_full_name,
                'seller_id': t['seller'].get('customer_id') or '',
                'price_btc': 'at [b]{}[/b] $/BTC'.format(t['btc_price']),
                'amount_usd': 'with [b]{}$ US[/b]'.format(t['usd_amount']),
                'date': t['date'],
                'from_to': '{} -> {}'.format(
                    t['seller']['btc_address'][:4] + '...' + t['seller']['btc_address'][-4:],
                    t['buyer']['btc_address'][:4] + '...' + t['buyer']['btc_address'][-4:],
                ),
                'blockchain_status': '[color={}][{}][/color]'.format(
                    '#d07050' if t.get('void') else ('#a0a060' if t.get('blockchain_status') != 'confirmed' else '#60b060'),
                    'void' if t.get('void') else (t.get('blockchain_status', 'unconfirmed')),
                ),
                'void': '1' if t.get('void') else '',
            })

#------------------------------------------------------------------------------

class TransactionsScreen(screen.AppScreen):

    transactions_to_be_verified = ListProperty([])
    verification_progress = 0
    selected_customer_id = None

    def on_enter(self, *args):
        self.ids.transactions_view.populate(selected_customer_id=self.selected_customer_id)

    def on_leave(self, *args):
        self.selected_customer_id = None

    def on_view_transaction_button_clicked(self):
        self.scr('one_transaction_screen').transaction_id = self.ids.transactions_view.selected_item.ids.tr_id.text
        self.scr_manager().current = 'one_transaction_screen'

    def on_seller_text_ref_pressed(self, *args):
        if _Debug:
            print('TransactionsScreen.on_seller_text_ref_pressed', args)
        transaction_id = args[0].replace('transaction_', '')
        tr = local_storage.read_transaction(transaction_id)
        if tr:
            customer_id = (tr.get('seller') or {}).get('customer_id') or ''
            if customer_id:
                customer_info = local_storage.read_customer_info(customer_id) or {}
                if customer_info:
                    self.scr('edit_customer_screen').customer_id = customer_id
                    self.scr_manager().current = 'edit_customer_screen'

    def on_buyer_text_ref_pressed(self, *args):
        if _Debug:
            print('TransactionsScreen.on_buyer_text_ref_pressed', args)
        transaction_id = args[0].replace('transaction_', '')
        tr = local_storage.read_transaction(transaction_id)
        if tr:
            customer_id = (tr.get('buyer') or {}).get('customer_id') or ''
            if customer_id:
                customer_info = local_storage.read_customer_info(customer_id) or {}
                if customer_info:
                    self.scr('edit_customer_screen').customer_id = customer_id
                    self.scr_manager().current = 'edit_customer_screen'
        
    def on_disable_transaction_button_clicked(self):
        transaction_id = self.ids.transactions_view.selected_item.ids.tr_id.text
        tr = local_storage.read_transaction(transaction_id)
        if tr:
            tr['void'] = True
            local_storage.write_transaction(transaction_id, tr)
            self.ids.transactions_view.populate(selected_customer_id=self.selected_customer_id)

    def on_print_pdf_transactions_button_clicked(self):
        selected_month = self.ids.select_month_button.text
        selected_year = self.ids.select_year_button.text
        if selected_month != '-' and selected_year == '-':
            return
        selected_transactions = []
        for t in local_storage.load_transactions_list():
            if self.selected_customer_id:
                if str(self.selected_customer_id) != str(t['buyer'].get('customer_id') or '') and str(self.selected_customer_id) != str(t['seller'].get('customer_id') or ''):
                    continue
            if t.get('blockchain_status') != 'confirmed':
                if not t.get('void'):
                    continue
            if selected_year != '-' and not t['date'].endswith(selected_year):
                continue
            if selected_month != '-' and not t['date'].startswith(selected_month[:3]):
                continue
            selected_transactions.append(t)
        output_filename = 'transactions'
        if selected_year != '-':
            output_filename += '_' + selected_year
        if selected_month != '-':
            output_filename += '_' + selected_month
        output_filename += '.pdf'
        pdf_report = render_pdf.build_transactions_report(
            selected_transactions=selected_transactions,
            selected_month=selected_month,
            selected_year=selected_year,
            pdf_filepath=os.path.join(local_storage.reports_dir(), output_filename),
        )
        system.open_path_in_os(pdf_report['filename'])

    def on_print_csv_transactions_button_clicked(self):
        selected_month = self.ids.select_month_button.text
        selected_year = self.ids.select_year_button.text
        if selected_month != '-' and selected_year == '-':
            return
        selected_transactions = []
        for t in local_storage.load_transactions_list():
            if self.selected_customer_id:
                if str(self.selected_customer_id) != str(t['buyer'].get('customer_id') or '') and str(self.selected_customer_id) != str(t['seller'].get('customer_id') or ''):
                    continue
            if t.get('blockchain_status') != 'confirmed':
                continue
            if selected_year != '-' and not t['date'].endswith(selected_year):
                continue
            if selected_month != '-' and not t['date'].startswith(selected_month[:3]):
                continue
            selected_transactions.append(t)
        output_filename = 'transactions'
        if selected_year != '-':
            output_filename += '_' + selected_year
        if selected_month != '-':
            output_filename += '_' + selected_month
        output_filename += '.csv'
        csv_report_filename = render_csv.build_transactions_report(
            selected_transactions=selected_transactions,
            csv_filepath=os.path.join(local_storage.reports_dir(), output_filename),
        )
        system.open_path_in_os(csv_report_filename)

    def on_verfy_transactions_button_clicked(self):
        cur_settings = local_storage.read_settings()
        try:
            contract_expiration_period_days = int(cur_settings.get('contract_expiration_period_days'))
        except:
            contract_expiration_period_days = 0
        self.ids.verify_contracts_button.disabled = True
        self.verification_progress = 0
        for t in local_storage.load_transactions_list():
            if self.selected_customer_id:
                if str(self.selected_customer_id) != str(t['buyer'].get('customer_id') or '') and str(self.selected_customer_id) != str(t['seller'].get('customer_id') or ''):
                    continue
            if t.get('blockchain_status') == 'confirmed':
                continue
            if t.get('void'):
                continue
            if contract_expiration_period_days:
                contract_local_time = datetime.datetime.strptime(
                    '{} {}'.format(t['date'], t['time']),
                    '%b %d %Y %I:%M %p')
                t_now = datetime.datetime.now()
                if (t_now - contract_local_time).days > contract_expiration_period_days:
                    continue
            self.transactions_to_be_verified.append(t)
            if len(self.transactions_to_be_verified) >= 10:
                break
        if _Debug:
            print('transactions to be verified: %d' % len(self.transactions_to_be_verified))
        Clock.schedule_once(self.verify_next_transaction, 0)

    def verify_next_transaction(self, *args):
        if not self.transactions_to_be_verified:
            self.ids.verify_contracts_button.disabled = False
            return
        transaction_details = self.transactions_to_be_verified.pop(0)
        self.verification_progress += 1
        if _Debug:
            print('verify_next_transaction %r  progress is %r' % (
                transaction_details['transaction_id'], self.verification_progress))
        confirmed = False
        cur_settings = local_storage.read_settings()
        if transaction_details.get('lightning'):
            if not transaction_details.get('void'):
                transaction_details['blockchain_status'] = 'confirmed'
                transaction_details['confirmed_time'] = datetime.datetime.now().strftime("%b %d %Y %I:%M %p")
                local_storage.write_transaction(transaction_details['transaction_id'], transaction_details)
                confirmed = True
        else:
            matching_transactions = btc_util.verify_contract(
                contract_details=transaction_details,
                price_precision_matching_percent=float(cur_settings.get('price_precision_matching_percent', '0.0')),
                price_precision_fixed_amount=float(cur_settings.get('price_precision_fixed_amount', '0.0')),
                time_matching_seconds_before=float(cur_settings.get('time_matching_seconds_before', '0.0')),
                time_matching_seconds_after=float(cur_settings.get('time_matching_seconds_after', '0.0')),
            )
            if len(matching_transactions) == 1:
                transaction_details['blockchain_status'] = 'confirmed'
                transaction_details['blockchain_tx_info'] = matching_transactions[0]
                transaction_details['confirmed_time'] = datetime.datetime.now().strftime("%b %d %Y %I:%M %p")
                local_storage.write_transaction(transaction_details['transaction_id'], transaction_details)
                confirmed = True
        if confirmed:
            for transaction_item in self.ids.transactions_view.data:
                if transaction_item['tr_id'] == transaction_details['transaction_id']:
                    transaction_item['blockchain_status'] = '[color={}][{}][/color]'.format('#60b060', 'confirmed')
                    self.ids.transactions_view.refresh_from_data()
        Clock.schedule_once(self.verify_next_transaction, 5.0)
