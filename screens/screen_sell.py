from kivy.app import App

#------------------------------------------------------------------------------

from components.screen import AppScreen
from storage import local_storage

#------------------------------------------------------------------------------

kv = """
<SellScreen>:
    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'bottom'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .08
            padding: 10
            spacing: 2
            RoundedButton:
                id: sell_select_customer_button
                text: "Select Customer"
                width: 120
                size_hint_x: None
                on_release: root.on_sell_select_customer_button_clicked()
            RoundedButton:
                text: "Clear"
                width: 120
                size_hint_x: None
                on_release: root.clean_input_fields()
            RoundedButton:
                text: "PDF file"
                width: 120
                size_hint_x: None
            RoundedButton: 
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
                text: "First name:"
            TextInput:
                id: sell_person_first_name_input
                text: ""
            Label:
                text: "Last name:"
            TextInput:
                id: sell_person_last_name_input
                text: ""
            Label:
                text: "Phone:"
            TextInput:
                id: sell_person_phone_input
                text: ""
            Label:
                text: "E-mail:"
            TextInput:
                id: sell_person_email_input
                text: ""
            Label:
                text: "Address:"
            TextInput:
                id: sell_person_address_input
                text: ""
            Label:
                text: "BTC price (US $ / BTC):"
            TextInput:
                id: sell_btc_price_input
                text: ""
            Label:
                text: "Amount (US $):"
            TextInput:
                id: sell_usd_amount_input
                text: ""
            Label:
                text: "Destination BitCoin address:"
            TextInput:
                id: sell_destination_address_input
                text: ""
"""

#------------------------------------------------------------------------------

class SellScreen(AppScreen):

    selected_customer_id = None

    def clean_input_fields(self):
        self.ids.sell_person_first_name_input.text = ''
        self.ids.sell_person_last_name_input.text = ''
        self.ids.sell_person_phone_input.text = ''
        self.ids.sell_person_email_input.text = ''
        self.ids.sell_person_address_input.text = ''
        self.ids.sell_btc_price_input.text = ''
        self.ids.sell_usd_amount_input.text = ''
        self.ids.sell_destination_address_input.text = ''
        self.selected_customer_id = None

    def populate_customer_info_fields(self, customer_info):
        self.ids.sell_person_first_name_input.text = customer_info.get('first_name') or ''
        self.ids.sell_person_last_name_input.text = customer_info.get('last_name') or ''
        self.ids.sell_person_phone_input.text = customer_info.get('phone') or ''
        self.ids.sell_person_email_input.text = customer_info.get('email') or ''
        self.ids.sell_person_address_input.text = customer_info.get('address') or ''

    def on_pre_enter(self, *args):
        if self.selected_customer_id is None:
            self.clean_input_fields()

    def on_sell_select_customer_button_clicked(self, *args):
        select_customer_screen = App.get_running_app().root.ids.scr_manager.get_screen('select_customer_screen')
        select_customer_screen.clear_selected_items()
        select_customer_screen.customer_selected_callback = self.on_customer_selected
        App.get_running_app().root.ids.scr_manager.current = 'select_customer_screen'

    def on_customer_selected(self, selected_customer_id):
        self.selected_customer_id = selected_customer_id
        customer_info = local_storage.read_customer_info(self.selected_customer_id)
        self.populate_customer_info_fields(customer_info)
        App.get_running_app().root.ids.scr_manager.current = 'sell_screen'
