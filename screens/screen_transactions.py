
from components import screen
from components import list_view

from storage import local_storage

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
    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'bottom'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .08
            padding: 10
            spacing: 2
            RoundedButton:
                id: view_transaction_button
                text: 'open'
                width: 160
                size_hint_x: None
                disabled: True
                on_release: root.on_view_transaction_button_clicked()
            RoundedButton:
                text: 'print transactions'
                width: 160
                size_hint_x: None
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        TransactionsView:
            id: transactions_view
"""

#------------------------------------------------------------------------------

class TransactionsView(list_view.SelectableRecycleView):

    def __init__(self, **kwargs):
        super(TransactionsView, self).__init__(**kwargs)
        self.data = [{
            'tr_id': str(i['transaction_id']),
            'tr_type': '{}'.format('bought' if i['contract_type'] == 'purchase' else 'sold'),
            'buyer': '[b]{} {}[/b]'.format(i['buyer']['first_name'], i['buyer']['last_name']),
            'amount_btc': '[b]{}[/b] BTC {}'.format(i['btc_amount'], 'from' if i['contract_type'] == 'purchase' else 'to'),
            'seller': '[b]{} {}[/b]'.format(i['seller']['first_name'], i['seller']['last_name']),
            'price_btc': 'at [b]{}[/b] $/BTC'.format(i['btc_price']),
            'amount_usd': 'with [b]{}$ US[/b]'.format(i['usd_amount']),
            'date': i['date'],
            'from_to': '{} -> {}'.format(i['seller']['btc_address'], i['buyer']['btc_address']),
            'blockchain_status': '[color=#b0b070]{}[/color]'.format(i.get('blockchain_status', 'unconfirmed')),
        } for i in local_storage.load_transactions_list()]

    def on_selection_applied(self, item, index, is_selected, prev_selected):
        self.parent.parent.ids.view_transaction_button.disabled = not is_selected

#------------------------------------------------------------------------------

class TransactionsScreen(screen.AppScreen):

    def on_view_transaction_button_clicked(self):
        self.scr('one_transaction_screen').transaction_id = self.ids.transactions_view.selected_item.ids.tr_id.text
        self.scr_manager().current = 'one_transaction_screen'
