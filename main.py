from kivy.app import App

from kivy.config import Config

from kivy.lang import Builder

from kivy.properties import BooleanProperty  # @UnresolvedImport

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior

#------------------------------------------------------------------------------

sample_data = [
    {
        'tr_id': '1',
        'tr_type': 'buy',
        'buyer': 'Vincent Cate',
        'seller': 'John Smith',
        'addr_from': '1FiTczw1GeaEdMoGbQWngWT8gCirYuzfne',
        'addr_to': '15f66HZrumZ5eW6RuA5A2JewBasBh44gB7',
        'amount_btc': '0.009804',
        'amount_usd': '100.0',
        'price_btc': '10221.5',
        'date': 'Sept 4, 2020 9:04 AM',
    }, {
        'tr_id': '2',
        'tr_type': 'sell',
        'buyer': 'Marry Jane',
        'seller': 'Vincent Cate',
        'addr_from': '3AGZzm6QMmYG8e7JzRuAUPnSYnXfHRtFSZ',
        'addr_to': '15f66HZrumZ5eW6RuA5A2JewBasBh44gB7',
        'amount_usd': '500.0',
        'amount_btc': '0.049523',
        'price_btc': '10121.25',
        'date': 'Sept 5, 2020 11:08 AM',
    }, {
        'tr_id': '3',
        'tr_type': 'buy',
        'buyer': 'Vincent Cate',
        'seller': 'John Smith',
        'addr_from': '17jEt5PSWwVt8WZFHZ3urE7fQ4m7Y28eUo',
        'addr_to': '15f66HZrumZ5eW6RuA5A2JewBasBh44gB7',
        'amount_usd': '2000.0',
        'amount_btc': '0.180243',
        'price_btc': '10033.12',
        'date': 'Sept 9, 2020 5:34 PM',
    }
]

#------------------------------------------------------------------------------

Builder.load_string("""
#:import NoTransition kivy.uix.screenmanager.NoTransition

<Label>:
    markup: True
    color: 0, 0, 0, 1

<Button>:
    markup: True
    color: 1, 1, 1, 1

<MainWindow>:
    color: 0, 0, 0, 1
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .1
            padding: 10
            Button:
                text: 'Buy BTC'
                on_press: _screen_manager.current = 'screen1'
            Button:
                text: 'Sell BTC'
                on_press: _screen_manager.current = 'screen2'
            Button:
                text: 'Transactions'
                on_press: _screen_manager.current = 'screen3'

    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'bottom'
        ScreenManager:
            size_hint: 1, .9
            id: _screen_manager
            transition: NoTransition()
            Screen:
                name: 'screen0'
                Label:
                    color: 0, 0, 0, 1 
                    markup: True
                    text: '[size=24]BitCoin Simple Contracts[/size]'

            Screen:
                name: 'screen1'
                GridLayout:
                    cols: 2
                    padding: 10
                    row_force_default: True
                    row_default_height: 40
                    Label:
                        text: "Seller:"
                    TextInput: 
                        text: "John Smith"
                    Label:
                        text: "BTC price (US $ / BTC):"
                    TextInput: 
                        text: "10200"
                    Label:
                        text: "Amount (US $):"
                    TextInput: 
                        text: "1000"
                    Label:
                        text: "Receiving BitCoin address:"
                    TextInput: 
                        text: "1FiTczw1GeaEdMoGbQWngWT8gCirYuzfne"
                    Button:
                        text: "Save as PDF"
                    Button: 
                        text: "Print"

            Screen:
                name: 'screen2'
                GridLayout:
                    cols: 2
                    padding: 10
                    row_force_default: True
                    row_default_height: 40
                    Label:
                        text: "Buyer:"
                    TextInput: 
                        text: "John Smith"
                    Label:
                        text: "BTC price (US $ / BTC):"
                    TextInput: 
                        text: "10200"
                    Label:
                        text: "Amount (US $):"
                    TextInput: 
                        text: "1000"
                    Label:
                        text: "Destination BitCoin address:"
                    TextInput: 
                        text: "1FiTczw1GeaEdMoGbQWngWT8gCirYuzfne"
                    Button:
                        text: "Save as PDF"
                    Button: 
                        text: "Print"

            Screen:
                name: 'screen3'
                TransactionsView:
                    id: transactions_view

<TransactionRecord>:
    canvas.before:
        Color:
            rgba: (0.8, 0.8, 0.8, 1) if self.selected else (1, 1, 1, 1)
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

""")

#------------------------------------------------------------------------------ 

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')  # disable multi-touch

#------------------------------------------------------------------------------

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass


class TransactionRecord(RecycleDataViewBehavior, StackLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(TransactionRecord, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        if super(TransactionRecord, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        # if is_selected:
        #     print("selection changed to {0}".format(rv.data[index]))
        # else:
        #     print("selection removed for {0}".format(rv.data[index]))


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
        } for i in sample_data]


class MainWindow(FloatLayout):
    pass


class BitCoinContractsApp(App):

    def build(self):
        return MainWindow()


if __name__ == '__main__':
    BitCoinContractsApp().run()
