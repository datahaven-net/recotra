from kivy.properties import ObjectProperty  # @UnresolvedImport
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager

#------------------------------------------------------------------------------

from lib import render_pdf
from storage import local_storage

#------------------------------------------------------------------------------

kv = """
<WelcomeScreen@Screen>:
    Label:
        color: 0, 0, 0, 1 
        markup: True
        text: '[size=24]BitCoin Simple Contracts[/size]'


<ScreenManagement>:
    transition: NoTransition()
    customers_screen: customers_screen
    WelcomeScreen:
        id: welcome_screen
        name: 'welcome_screen'

    BuyScreen:
        id: buy_screen
        name: 'buy_screen'

    SellScreen:
        id: sell_screen
        name: 'sell_screen'

    TransactionsScreen:
        id: transactions_screen
        name: 'transactions_screen'

    CustomersScreen:
        id: customers_screen
        name: 'customers_screen'

    AddCustomerScreen:
        id: add_customer_screen
        name: 'add_customer_screen'

    CameraTakePictureScreen:
        id: camera_take_picture_screen
        name: 'camera_take_picture_screen'


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
                on_press: scr_manager.current = 'buy_screen'
                width: 120
                size_hint_x: None
            Button:
                text: 'Sell BTC'
                on_press: scr_manager.current = 'sell_screen'
                width: 120
                size_hint_x: None
            Button:
                text: 'Transactions'
                on_press: scr_manager.current = 'transactions_screen'
                width: 120
                size_hint_x: None
            Button:
                text: 'Customers'
                on_press: scr_manager.current = 'customers_screen'
                width: 120
                size_hint_x: None

    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'bottom'
        ScreenManagement:
            id: scr_manager
            size_hint: 1, .92
"""

#------------------------------------------------------------------------------

class ScreenManagement(ScreenManager):
    customers_screen = ObjectProperty(None)

    def on_buy_pdf_file_button_clicked(self):
        buy_contract = render_pdf.build_buy_contract()
        render_pdf.open_file(buy_contract['filename'])

    def on_buy_save_customer_button_clicked(self):
        person_name = self.ids.buy_person_name_input.text.strip()
        receive_address = self.ids.buy_receive_address_input.text.strip().lower()
        person_found = None
        person_found_pos = -1
        latest_customer_id = 0
#         for pos in range(len(_Customers)):
#             person = _Customers[pos]
#             if person['person_name'].lower() == person_name.lower():
#                 person_found = person
#                 person_found_pos = pos
#             if latest_customer_id < person['customer_id']:
#                 latest_customer_id = person['customer_id']
#         if person_found:
#             if not person_found['known_wallets'].count(receive_address):
#                 person_found['known_wallets'] = ','.join(person_found['known_wallets'].split(',') + [receive_address, ])
#                 _Customers[person_found_pos] = person_found
#                 local_storage.save_customers_list(_Customers)
#                 self.ids.customers_view.data = local_storage.make_customers_ui_data(_Customers)
#             return
#         new_person = {
#             'customer_id': latest_customer_id + 1,
#             'person_name': person_name,
#             'known_wallets': receive_address,
#         }
#         _Customers.append(new_person)
#         local_storage.save_customers_list(_Customers)
#         self.ids.customers_view.data = local_storage.make_customers_ui_data(_Customers)

#------------------------------------------------------------------------------

class MainWindow(FloatLayout):
    pass
