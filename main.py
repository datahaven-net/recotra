import sys
import logging

#------------------------------------------------------------------------------

from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder
from kivy.logger import Logger, LOG_LEVELS

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

Window.clearcolor = (1, 1, 1, 1)

#------------------------------------------------------------------------------

kv = """
#:import NoTransition kivy.uix.screenmanager.NoTransition
#:import Window kivy.core.window.Window
#:import fa_icon components.webfont.fa_icon
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
# print(kv)
Builder.load_string(kv)

#------------------------------------------------------------------------------

class BitCoinContractsApp(App):

    def build(self):
        level = LOG_LEVELS.get('debug')  #  if len(sys.argv) > 2 else LOG_LEVELS.get('info')
        Logger.setLevel(level=level)
        logging.getLogger().setLevel(logging.DEBUG)

        local_storage.init()
        screen_transactions._Transactions = local_storage.load_transactions_list()
        screen_customers._Customers = local_storage.load_customers_list()
        return main_window.MainWindow()

    def on_stop(self):
        self.root.ids.scr_manager.get_screen('customers_screen').clear_selected_items()

#------------------------------------------------------------------------------

if __name__ == '__main__':
    BitCoinContractsApp().run()
