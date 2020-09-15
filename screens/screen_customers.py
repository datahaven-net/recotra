from kivy.app import App
from kivy.properties import ObjectProperty  # @UnresolvedImport
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView

#------------------------------------------------------------------------------

from components import list_view
from storage import local_storage

#------------------------------------------------------------------------------

_Customers = []

#------------------------------------------------------------------------------

kv = """
<CustomerRecord>:
    canvas.before:
        Color:
            rgba: (.9, .9, 1, 1) if self.selected else (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    orientation: 'lr-tb'
    height: 70
    size_hint_y: None
    customer_id: 'customer_id'
    person_name: 'person_name'
    known_wallets: 'known_wallets'
    Label:
        id: customer_id
        text: root.customer_id
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

<CustomersView>:
    viewclass: 'CustomerRecord'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: False

<CustomersScreen>:
    customer_delete_button: customer_delete_button
    BoxLayout:
        orientation: 'vertical'
        CustomersView:
            id: customers_view
        BoxLayout:
            orientation: 'horizontal'
            # size_hint: 1, .08
            padding: 10
            spacing: 2
            Button:
                id: customer_add_button
                text: 'Add Customer'
                width: 120
                size_hint_x: None
                on_press: root.on_customers_add_button_clicked()
            Button:
                id: customer_delete_button
                text: 'Erase Customer'
                width: 120
                size_hint_x: None
                disabled: True
                on_press: root.on_customers_delete_button_clicked()
"""

#------------------------------------------------------------------------------

class CustomerRecord(list_view.SelectableRecord):

    def apply_selection(self, rv, index, is_selected):
        App.get_running_app().root.ids.scr_manager.get_screen('customers_screen').customer_delete_button.disabled = not is_selected
        return list_view.SelectableRecord.apply_selection(self, rv, index, is_selected)

#------------------------------------------------------------------------------

class CustomersView(RecycleView):

    def __init__(self, **kwargs):
        global _Customers
        super(CustomersView, self).__init__(**kwargs)
        self.data = local_storage.make_customers_ui_data(_Customers)

#------------------------------------------------------------------------------

class CustomersScreen(Screen):
    customer_delete_button = ObjectProperty(None)

    def on_customers_add_button_clicked(self):
        App.get_running_app().root.ids.scr_manager.current = 'add_customer_screen'

    def on_customers_delete_button_clicked(self):
        print('456')

