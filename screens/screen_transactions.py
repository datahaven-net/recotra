from kivy.uix.recycleview import RecycleView

#------------------------------------------------------------------------------

_Transactions = []

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

<TransactionsScreen@Screen>:
    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'bottom'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .08
            padding: 10
            spacing: 2
            RoundedButton:
                text: 'Print transactions'
                width: 160
                size_hint_x: None
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        TransactionsView:
            id: transactions_view
"""

#------------------------------------------------------------------------------

sample_transactions = [
    {
        'tr_id': 1,
        'tr_type': 'buy',
        'buyer': 'Vincent Cate',
        'seller': 'John Smith',
        'addr_from': '1FiTczw1GeaEdMoGbQWngWT8gCirYuzfne',
        'addr_to': '15f66HZrumZ5eW6RuA5A2JewBasBh44gB7',
        'amount_btc': 0.009804,
        'amount_usd': 100.0,
        'price_btc': 10221.5,
        'date': 'Sept 4, 2020 9:04 AM',
    }, {
        'tr_id': 2,
        'tr_type': 'sell',
        'buyer': 'Marry Jane',
        'seller': 'Vincent Cate',
        'addr_from': '3AGZzm6QMmYG8e7JzRuAUPnSYnXfHRtFSZ',
        'addr_to': '15f66HZrumZ5eW6RuA5A2JewBasBh44gB7',
        'amount_usd': 500.0,
        'amount_btc': 0.049523,
        'price_btc': 10121.25,
        'date': 'Sept 5, 2020 11:08 AM',
    }, {
        'tr_id': 3,
        'tr_type': 'buy',
        'buyer': 'Vincent Cate',
        'seller': 'John Smith',
        'addr_from': '17jEt5PSWwVt8WZFHZ3urE7fQ4m7Y28eUo',
        'addr_to': '15f66HZrumZ5eW6RuA5A2JewBasBh44gB7',
        'amount_usd': 2000.0,
        'amount_btc': 0.180243,
        'price_btc': 10033.12,
        'date': 'Sept 9, 2020 5:34 PM',
    }
]

#------------------------------------------------------------------------------

class TransactionsView(RecycleView):

    def __init__(self, **kwargs):
        super(TransactionsView, self).__init__(**kwargs)
        self.data = [{
            'tr_id': str(i['tr_id']),
            'buyer': i['buyer'],
            'tr_type': '{}'.format('bought' if i['tr_type'] == 'buy' else 'sold'),
            'amount_btc': '[b]{}[/b] BTC {}'.format(i['amount_btc'], 'from' if i['tr_type'] == 'buy' else 'to'),
            'seller': '[b]{}[/b]'.format(i['seller']),
            'price_btc': 'at [b]{}[/b] $/BTC'.format(i['price_btc']),
            'amount_usd': 'with [b]{}$ US[/b]'.format(i['amount_usd']),
            'date': i['date'],
            'from_to': '{} -> {}'.format(i['addr_from'], i['addr_to']),
        } for i in sample_transactions]

#------------------------------------------------------------------------------
