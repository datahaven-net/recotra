import os
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
from components import list_view
from components import main_window

from screens import screen_buy, screen_edit_customer
from screens import screen_sell
from screens import screen_customers
from screens import screen_add_customer
from screens import screen_edit_customer
from screens import screen_select_customer
from screens import screen_transactions
from screens import screen_one_transaction
from screens import screen_settings

from storage import local_storage

#------------------------------------------------------------------------------ 

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')  # disable multi-touch
Config.set('graphics', 'resizable', True)

Window.clearcolor = (1, 1, 1, 1)

os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'

#------------------------------------------------------------------------------

kv = """
#:import NoTransition kivy.uix.screenmanager.NoTransition
#:import Window kivy.core.window.Window
#:import fa_icon components.webfont.fa_icon
""" + '\n'.join([
    labels.kv,
    buttons.kv,
    list_view.kv,
    screen_buy.kv,
    screen_sell.kv,
    screen_customers.kv,
    screen_add_customer.kv,
    screen_edit_customer.kv,
    screen_select_customer.kv,
    screen_transactions.kv,
    screen_one_transaction.kv,
    screen_settings.kv,
    main_window.kv,
])
Builder.load_string(kv)

#------------------------------------------------------------------------------

class BitCoinContractsApp(App):

    def build(self):
        level = LOG_LEVELS.get('debug')
        Logger.setLevel(level=level)
        logging.getLogger().setLevel(logging.DEBUG)

        local_storage.init()
        self.title = 'Regulatory Compliant Trader'
        self.icon = './icons/btcusd.ico'
        self.main_window = main_window.MainWindow()
        return self.main_window

    def on_stop(self):
        self.root.ids.scr_manager.get_screen('customers_screen').clear_selected_items()

#------------------------------------------------------------------------------

if __name__ == '__main__':
    BitCoinContractsApp().run()
