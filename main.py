from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder

#------------------------------------------------------------------------------

from components import buttons
from components import labels
from components import main_window

from screens import screen_buy
from screens import screen_sell
from screens import screen_transactions
from screens import screen_customers
from screens import screen_add_customer

from storage import local_storage

#------------------------------------------------------------------------------ 

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')  # disable multi-touch
Config.set('graphics', 'resizable', True)

#------------------------------------------------------------------------------

kv = """
#:import NoTransition kivy.uix.screenmanager.NoTransition
#:import Window kivy.core.window.Window
""" + '\n'.join([
    labels.kv,
    buttons.kv,
    screen_buy.kv,
    screen_sell.kv,
    screen_transactions.kv,
    screen_customers.kv,
    screen_add_customer.kv,
    main_window.kv,
])
print(kv)
Builder.load_string(kv)

#------------------------------------------------------------------------------

class BitCoinContractsApp(App):

    def build(self):
        screen_transactions._Transactions = local_storage.load_transactions_list()
        screen_customers._Customers = local_storage.load_customers_list()
        return main_window.MainWindow()

#------------------------------------------------------------------------------

if __name__ == '__main__':
    BitCoinContractsApp().run()
