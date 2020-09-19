import datetime

#------------------------------------------------------------------------------

from kivy.app import App

#------------------------------------------------------------------------------

from lib import render_pdf
from components.screen import AppScreen
from storage import local_storage

#------------------------------------------------------------------------------

kv = """
<BuyScreen@Screen>:
    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'bottom'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .08
            padding: 10
            spacing: 2
            RoundedButton:
                id: save_customer_button
                text: "Select Customer"
                width: 120
                size_hint_x: None
                on_release: root.on_select_customer_button_clicked()
            RoundedButton:
                text: "Clear"
                width: 120
                size_hint_x: None
                on_release: root.clean_input_fields()
            RoundedButton:
                text: "Print!"
                width: 120
                size_hint_x: None
                on_release: root.on_pdf_file_button_clicked()
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
                id: person_first_name_input
                text: ""
            Label:
                text: "Last name:"
            TextInput:
                id: person_last_name_input
                text: ""
            Label:
                text: "Phone:"
            TextInput:
                id: person_phone_input
                text: ""
            Label:
                text: "E-mail:"
            TextInput:
                id: person_email_input
                text: ""
            Label:
                text: "Address:"
            TextInput:
                id: person_address_input
                text: ""
            Label:
                text: "BTC price (US $ / BTC):"
            TextInput:
                id: btc_price_input
                text: ""
            Label:
                text: "Amount (US $):"
            TextInput:
                id: usd_amount_input
                text: ""
            Label:
                text: "BTC Amount:"
            TextInput:
                id: btc_amount_input
                text: ""
            Label:
                text: "Receiving BitCoin address:"
            TextInput:
                id: receive_address_input
                text: ""

"""

#------------------------------------------------------------------------------

class BuyScreen(AppScreen):

    selected_customer_id = None
    selected_custoimer_info = None

    def clean_input_fields(self):
        self.ids.person_first_name_input.text = ''
        self.ids.person_last_name_input.text = ''
        self.ids.person_phone_input.text = ''
        self.ids.person_email_input.text = ''
        self.ids.person_address_input.text = ''
        self.ids.btc_price_input.text = ''
        self.ids.usd_amount_input.text = ''
        self.ids.btc_amount_input.text = ''
        self.ids.receive_address_input.text = ''
        self.selected_customer_id = None

    def populate_customer_info_fields(self, customer_info):
        self.ids.person_first_name_input.text = customer_info.get('first_name') or ''
        self.ids.person_last_name_input.text = customer_info.get('last_name') or ''
        self.ids.person_phone_input.text = customer_info.get('phone') or ''
        self.ids.person_email_input.text = customer_info.get('email') or ''
        self.ids.person_address_input.text = customer_info.get('address') or ''

    def on_pre_enter(self, *args):
        if self.selected_customer_id is None:
            self.clean_input_fields()

    def on_select_customer_button_clicked(self, *args):
        select_customer_screen = App.get_running_app().root.ids.scr_manager.get_screen('select_customer_screen')
        select_customer_screen.customer_selected_callback = self.on_customer_selected
        select_customer_screen.clear_selected_items()
        App.get_running_app().root.ids.scr_manager.current = 'select_customer_screen'

    def on_customer_selected(self, selected_customer_id):
        self.selected_customer_id = selected_customer_id
        self.selected_custoimer_info = local_storage.read_customer_info(self.selected_customer_id)
        self.populate_customer_info_fields(self.selected_custoimer_info)
        App.get_running_app().root.ids.scr_manager.current = 'buy_screen'

    def on_pdf_file_button_clicked(self):
        t_now = datetime.datetime.now()
        buy_contract = render_pdf.build_buy_contract(
            customer_info=self.selected_custoimer_info,
            contract_info=dict(
                btc_price=self.ids.btc_price_input.text,
                usd_amount=self.ids.usd_amount_input.text,
                btc_amount=self.ids.btc_amount_input.text,
                receive_address=self.ids.receive_address_input.text,
                date=t_now.strftime("%b %d %Y"),
                time=t_now.strftime("%H:%M %p"),
            ),
        )
        render_pdf.open_file(buy_contract['filename'])
