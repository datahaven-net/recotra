from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager

#------------------------------------------------------------------------------

kv = """
<VerticalScrollView@ScrollView>:
    do_scroll_x: False


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

    CustomersScreen:
        id: customers_screen
        name: 'customers_screen'

    AddCustomerScreen:
        id: add_customer_screen
        name: 'add_customer_screen'

    SelectCustomerScreen:
        id: select_customer_screen
        name: 'select_customer_screen'

    TransactionsScreen:
        id: transactions_screen
        name: 'transactions_screen'

    OneTransactionScreen:
        id: one_transaction_screen
        name: 'one_transaction_screen'


<MainWindow>:
    color: 0, 0, 0, 1
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: None, None
            height: self.minimum_height
            padding: 10
            spacing: 2
            RoundedButton:
                text: 'Buy BTC'
                on_press: scr_manager.current = 'buy_screen'
                width: 120
                size_hint_x: None
            RoundedButton:
                text: 'Sell BTC'
                on_press: scr_manager.current = 'sell_screen'
                width: 120
                size_hint_x: None
            RoundedButton:
                text: 'Transactions'
                on_press: scr_manager.current = 'transactions_screen'
                width: 120
                size_hint_x: None
            RoundedButton:
                text: 'Customers'
                on_press: scr_manager.current = 'customers_screen'
                width: 120
                size_hint_x: None
        ScreenManagement:
            id: scr_manager
            size_hint: 1, 1
"""

#------------------------------------------------------------------------------

class ScreenManagement(ScreenManager):
    pass

#------------------------------------------------------------------------------

class MainWindow(FloatLayout):
    pass
