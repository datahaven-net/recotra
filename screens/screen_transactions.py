import os

#------------------------------------------------------------------------------

from components import screen
from components import list_view

from storage import local_storage

from lib import system
from lib import render_pdf
from lib import render_csv

#------------------------------------------------------------------------------

kv = """
<TransactionRecord@SelectableRecord>:

    canvas.before:
        Color:
            rgba: (.9, .9, 1, 1) if self.selected else (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size

    orientation: 'lr-tb'
    height: 70
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

    Label:
        id: tr_id
        text: root.tr_id
        size_hint: None, 0.36
        width: 40
    Label:
        id: buyer
        text: root.buyer
        bold: True
        size_hint: None, 0.36
        width: self.texture_size[0] + 10
    Label:
        id: tr_type
        text: root.tr_type
        size_hint: None, 0.36
        width: self.texture_size[0] + 10
    Label:
        id: amount_btc
        text: root.amount_btc
        markup: True
        size_hint: None, 0.36
        width: self.texture_size[0] + 10
    Label:
        id: seller
        text: root.seller
        markup: True
        size_hint: None, 0.36
        width: self.texture_size[0] + 10
    Label:
        id: price_btc
        text: root.price_btc
        markup: True
        size_hint: None, 0.36
        width: self.texture_size[0] + 10
    Label:
        id: amount_usd
        text: root.amount_usd
        markup: True
        size_hint: None, 0.36
        width: self.texture_size[0] + 10
    Label:
        id: date
        text: root.date
        size_hint: None, 0.36
        width: self.texture_size[0] + 10
    Label:
        id: from_to
        text: root.from_to
        font_name: 'DejaVuSans'
        font_size: 12
        size_hint: None, 0.3
        width: self.texture_size[0] + 10
    Label:
        id: blockchain_status
        text: root.blockchain_status
        size_hint: None, 0.3
        width: self.texture_size[0] + 10


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
            padding: 10
            spacing: 2

            RoundedButton:
                id: view_transaction_button
                text: 'view contract'
                width: self.texture_size[0] + dp(20)
                size_hint_x: None
                disabled: True
                on_release: root.on_view_transaction_button_clicked()

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
                values: '-', '2021', '2020', '2019'

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

"""

#------------------------------------------------------------------------------

class TransactionsView(list_view.SelectableRecycleView):

    def __init__(self, **kwargs):
        super(TransactionsView, self).__init__(**kwargs)
        self.data = []

    def on_selection_applied(self, item, index, is_selected, prev_selected):
        self.parent.parent.ids.view_transaction_button.disabled = not is_selected

    def populate(self):
        self.data = [{
            'tr_id': str(t['transaction_id']),
            'tr_type': '{}'.format('bought' if t['contract_type'] == 'purchase' else 'sold'),
            'buyer': '[b]{} {}[/b]'.format(t['buyer']['first_name'], t['buyer']['last_name']),
            'amount_btc': '[b]{}[/b] BTC {}'.format(t['btc_amount'], 'from' if t['contract_type'] == 'purchase' else 'to'),
            'seller': '[b]{} {}[/b]'.format(t['seller']['first_name'], t['seller']['last_name']),
            'price_btc': 'at [b]{}[/b] $/BTC'.format(t['btc_price']),
            'amount_usd': 'with [b]{}$ US[/b]'.format(t['usd_amount']),
            'date': t['date'],
            'from_to': '{} -> {}'.format(t['seller']['btc_address'], t['buyer']['btc_address']),
            'blockchain_status': '[color={}][{}][/color]'.format(
                '#a0a060' if t.get('blockchain_status') != 'confirmed' else '#60b060',
                t.get('blockchain_status', 'unconfirmed'),
            ),
        } for t in local_storage.load_transactions_list()]

#------------------------------------------------------------------------------

class TransactionsScreen(screen.AppScreen):


    def on_enter(self, *args):
        self.ids.transactions_view.populate()

    def on_view_transaction_button_clicked(self):
        self.scr('one_transaction_screen').transaction_id = self.ids.transactions_view.selected_item.ids.tr_id.text
        self.scr_manager().current = 'one_transaction_screen'

    def on_print_pdf_transactions_button_clicked(self):
        selected_month = self.ids.select_month_button.text
        selected_year = self.ids.select_year_button.text
        if selected_month != '-' and selected_year == '-':
            return
        selected_transactions = []
        for t in local_storage.load_transactions_list():
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
        output_filename += '.pdf'
        pdf_report = render_pdf.build_transactions_report(
            selected_transactions=selected_transactions,
            selected_month=selected_month,
            selected_year=selected_year,
            pdf_filepath=os.path.join(local_storage.reports_dir(), output_filename),
        )
        system.open_system_explorer(pdf_report['filename'])

    def on_print_csv_transactions_button_clicked(self):
        selected_month = self.ids.select_month_button.text
        selected_year = self.ids.select_year_button.text
        if selected_month != '-' and selected_year == '-':
            return
        selected_transactions = []
        for t in local_storage.load_transactions_list():
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
        system.open_system_explorer(csv_report_filename)
