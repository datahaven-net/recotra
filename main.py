import os

#------------------------------------------------------------------------------

from kivy.app import App

from kivy.config import Config

from kivy.lang import Builder

from kivy.properties import BooleanProperty  # @UnresolvedImport
from kivy.properties import ObjectProperty  # @UnresolvedImport

from kivy.uix.behaviors import FocusBehavior
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

#------------------------------------------------------------------------------

import local_storage
import render_pdf

#------------------------------------------------------------------------------

_Transactions = []
_Contacts = []

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

Builder.load_string("""
#:import NoTransition kivy.uix.screenmanager.NoTransition

<Label>:
    markup: True
    color: 0, 0, 0, 1

<Button>:
    markup: True
    background_color: 0,0,0,0
    color: 1, 1, 1, 1
    disabled_color: .8, .8, .8, 1
    background_disabled_normal: ''
    height: 30
    size_hint_y: None
    canvas.before:
        Color:
            rgba: (.3,.3,.3,1) if self.disabled else ((.1,.4,.7,1) if self.state == 'normal' else (.2,.5,.8,1)) 
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [6,]
        Color:
            rgba: (.4,.4,.4,1) if self.disabled else ((.3,.6,.9,1) if self.state == 'normal' else (.4,.7,1,1))
        RoundedRectangle:
            pos: self.pos[0]+2, self.pos[1]+2
            size: self.size[0]-4, self.size[1]-4
            radius: [5,]

<ScreenManagement>:
    transition: NoTransition()
    contacts_screen: contacts_screen
    WelcomeScreen:
        id: welcome_screen
        name: 'welcome_screen'
        Label:
            color: 0, 0, 0, 1 
            markup: True
            text: '[size=24]BitCoin Simple Contracts[/size]'

    BuyScreen:
        id: buy_screen
        name: 'buy_screen'
        AnchorLayout:
            anchor_x: 'left'
            anchor_y: 'bottom'
            BoxLayout:
                orientation: 'horizontal'
                size_hint: 1, .08
                padding: 10
                spacing: 2
                Button:
                    id: buy_save_contact_button
                    text: "Save Customer"
                    width: 120
                    size_hint_x: None
                    on_release: root.on_buy_save_contact_button_clicked()
                Button:
                    text: "PDF file"
                    width: 120
                    size_hint_x: None
                    on_release: root.on_buy_pdf_file_button_clicked()
                Button: 
                    text: "Print"
                    width: 120
                    size_hint_x: None
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'top'
            GridLayout:
                cols: 2
                padding: 10
                spacing: 2
                row_force_default: True
                row_default_height: 40
                Label:
                    text: "Seller:"
                TextInput:
                    id: buy_person_name_input
                    text: "John Smith"
                Label:
                    text: "BTC price (US $ / BTC):"
                TextInput:
                    id: buy_btc_price_input
                    text: "10200"
                Label:
                    text: "Amount (US $):"
                TextInput:
                    id: buy_usd_amount_input
                    text: "1000"
                Label:
                    text: "Receiving BitCoin address:"
                TextInput:
                    id: buy_receive_address_input
                    text: "1FiTczw1GeaEdMoGbQWngWT8gCirYuzfne"

    SellScreen:
        id: sell_screen
        name: 'sell_screen'
        AnchorLayout:
            anchor_x: 'left'
            anchor_y: 'bottom'
            BoxLayout:
                orientation: 'horizontal'
                size_hint: 1, .08
                padding: 10
                spacing: 2
                Button:
                    id: sell_save_contact_button
                    text: "Save Customer"
                    width: 120
                    size_hint_x: None
                    on_release: root.on_sell_save_contact_button_clicked()
                Button:
                    text: "PDF file"
                    width: 120
                    size_hint_x: None
                Button: 
                    text: "Print"
                    width: 120
                    size_hint_x: None
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'top'
            GridLayout:
                cols: 2
                padding: 10
                spacing: 2
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

    TransactionsScreen:
        id: transactions_screen
        name: 'transactions_screen'
        AnchorLayout:
            anchor_x: 'left'
            anchor_y: 'bottom'
            BoxLayout:
                orientation: 'horizontal'
                size_hint: 1, .08
                padding: 10
                spacing: 2
                Button:
                    text: 'Print transactions'
                    width: 160
                    size_hint_x: None
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'top'
            TransactionsView:
                id: transactions_view

    ContactsScreen:
        id: contacts_screen
        name: 'contacts_screen'
        contact_delete_button: contact_delete_button
        AnchorLayout:
            id: wrap1
            anchor_x: 'left'
            anchor_y: 'bottom'
            BoxLayout:
                id: wrap2
                orientation: 'horizontal'
                size_hint: 1, .08
                padding: 10
                spacing: 2
                Button:
                    id: contact_delete_button
                    text: 'Delete'
                    width: 120
                    size_hint_x: None
                    disabled: True
                    on_release: root.on_contacts_delete_button_clicked()
        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'top'
            ContactsView:
                id: contacts_view


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
            size_hint: 1, .08
            padding: 10
            spacing: 2
            Button:
                text: 'Buy BTC'
                on_press: _screen_manager.current = 'buy_screen'
                width: 120
                size_hint_x: None
            Button:
                text: 'Sell BTC'
                on_press: _screen_manager.current = 'sell_screen'
                width: 120
                size_hint_x: None
            Button:
                text: 'Transactions'
                on_press: _screen_manager.current = 'transactions_screen'
                width: 120
                size_hint_x: None
            Button:
                text: 'Customers'
                on_press: _screen_manager.current = 'contacts_screen'
                width: 120
                size_hint_x: None

    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'bottom'
        ScreenManagement:
            id: _screen_manager
            size_hint: 1, .92


<TransactionRecord>:
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


<ContactRecord>:
    canvas.before:
        Color:
            rgba: (.9, .9, 1, 1) if self.selected else (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    orientation: 'lr-tb'
    height: 70
    size_hint_y: None
    contact_id: 'contact_id'
    person_name: 'person_name'
    known_wallets: 'known_wallets'
    Label:
        id: contact_id
        text: root.contact_id
        size_hint: None, 0.5
        width: 40
    Label:
        id: person_name
        text: root.person_name
        bold: True
        size_hint: None, 0.5
        width: self.texture_size[0] + 10
    Label:
        id: known_wallets
        text: root.known_wallets
        size_hint: None, 0.5
        width: 160


<ContactsView>:
    viewclass: 'ContactRecord'
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
Config.set('graphics', 'resizable', True)

#------------------------------------------------------------------------------

class ScreenManagement(ScreenManager):
    contacts_screen = ObjectProperty(None)

    def on_buy_pdf_file_button_clicked(self):
        buy_contract = render_pdf.build_buy_contract()
        os.system('open "{}"'.format(buy_contract['filename']))

    def on_buy_save_contact_button_clicked(self):
        global _Contacts
        person_name = self.ids.buy_person_name_input.text.strip()
        receive_address = self.ids.buy_receive_address_input.text.strip().lower()
        person_found = None
        person_found_pos = -1
        latest_contact_id = 0
        for pos in range(len(_Contacts)):
            person = _Contacts[pos]
            if person['person_name'].lower() == person_name.lower():
                person_found = person
                person_found_pos = pos
            if latest_contact_id < person['contact_id']:
                latest_contact_id = person['contact_id']
        if person_found:
            if not person_found['known_wallets'].count(receive_address):
                person_found['known_wallets'] = ','.join(person_found['known_wallets'].split(',') + [receive_address, ])
                _Contacts[person_found_pos] = person_found
                local_storage.save_contacts_list(_Contacts)
                self.ids.contacts_view.data = local_storage.make_contacts_ui_data(_Contacts)
            return
        new_person = {
            'contact_id': latest_contact_id + 1,
            'person_name': person_name,
            'known_wallets': receive_address,
        }
        _Contacts.append(new_person)
        local_storage.save_contacts_list(_Contacts)
        self.ids.contacts_view.data = local_storage.make_contacts_ui_data(_Contacts)

    def on_contacts_delete_button_clicked(self):
        pass

#------------------------------------------------------------------------------

class WelcomeScreen(Screen):
    pass


class BuyScreen(Screen):
    pass


class SellScreen(Screen):
    pass


class ContactsScreen(Screen):
    contact_delete_button = ObjectProperty(None)


class TransactionsScreen(Screen):
    pass

#------------------------------------------------------------------------------

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):

    touch_deselect_last = BooleanProperty(True)


class SelectableRecord(RecycleDataViewBehavior, StackLayout):

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableRecord, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableRecord, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected

#------------------------------------------------------------------------------

class TransactionRecord(SelectableRecord):
    pass


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

class ContactRecord(SelectableRecord):

    def apply_selection(self, rv, index, is_selected):
        app = App.get_running_app()
        if app:
            app.root.ids._screen_manager.get_screen('contacts_screen').contact_delete_button.disabled = not is_selected
        return SelectableRecord.apply_selection(self, rv, index, is_selected)


class ContactsView(RecycleView):

    def __init__(self, **kwargs):
        global _Contacts
        super(ContactsView, self).__init__(**kwargs)
        self.data = local_storage.make_contacts_ui_data(_Contacts)

#------------------------------------------------------------------------------

class MainWindow(FloatLayout):
    pass


class BitCoinContractsApp(App):

    def build(self):
        global _Transactions
        global _Contacts
        _Transactions = local_storage.load_transactions_list()
        _Contacts = local_storage.load_contacts_list()
        return MainWindow()

#------------------------------------------------------------------------------

if __name__ == '__main__':
    BitCoinContractsApp().run()
