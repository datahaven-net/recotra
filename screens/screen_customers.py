from kivy.app import App
from kivy.properties import ObjectProperty  # @UnresolvedImport

#------------------------------------------------------------------------------

from components.screen import AppScreen
from components.list_view import SelectableRecycleView
from storage import local_storage

#------------------------------------------------------------------------------

kv = """
<CustomerRecord@SelectableRecord>:

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
    first_name: 'first_name'
    last_name: 'last_name'

    Label:
        id: customer_id
        text: root.customer_id
        size_hint: None, 0.5
        width: 40

    Label:
        id: first_name
        text: root.first_name
        bold: True
        size_hint: None, 0.5
        width: self.texture_size[0] + 10

    Label:
        id: last_name
        text: root.last_name
        size_hint: None, 0.5
        width: self.texture_size[0] + 10

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
    customer_edit_button: customer_edit_button
    customer_delete_button: customer_delete_button

    BoxLayout:
        orientation: 'vertical'

        CustomersView:
            id: customers_view
            size_hint: 1, 1

        BoxLayout:
            orientation: 'horizontal'
            size_hint: None, None
            height: self.minimum_height
            padding: 10
            spacing: 2

            RoundedButton:
                id: customer_add_button
                text: 'add'
                width: 120
                size_hint_x: None
                on_press: root.on_customers_add_button_clicked()

            RoundedButton:
                id: customer_edit_button
                text: 'modify'
                width: 120
                size_hint_x: None
                disabled: True
                on_press: root.on_customers_edit_button_clicked()

            RoundedButton:
                id: customer_delete_button
                text: 'erase'
                width: 120
                size_hint_x: None
                disabled: True
                on_press: root.on_customers_delete_button_clicked()
"""

#------------------------------------------------------------------------------

class CustomersView(SelectableRecycleView):

    def __init__(self, **kwargs):
        super(CustomersView, self).__init__(**kwargs)
        self.populate()

    def populate(self):
        self.data = []
        for customer_info in local_storage.make_customers_ui_data(
                customers_list=local_storage.load_customers_list(sort_by='customer_id'),
            ):
            self.data.append(customer_info)

    def on_selection_applied(self, item, index, is_selected, prev_selected):
        cust_screen = App.get_running_app().root.ids.scr_manager.get_screen('customers_screen')
        cust_screen.customer_delete_button.disabled = not is_selected
        cust_screen.customer_edit_button.disabled = not is_selected

#------------------------------------------------------------------------------

class CustomersScreen(AppScreen):

    customer_edit_button = ObjectProperty(None, allownone=True)
    customer_delete_button = ObjectProperty(None, allownone=True)

    def clear_selected_items(self):
        self.ids.customers_view.clear_selection()
        self.ids.customer_edit_button.disabled = True
        self.ids.customer_delete_button.disabled = True

    def on_leave(self, *args):
        self.clear_selected_items()

    def on_customers_add_button_clicked(self, *args):
        add_customer_screen = App.get_running_app().root.ids.scr_manager.get_screen('add_customer_screen')
        add_customer_screen.new_customer_id = None
        App.get_running_app().root.ids.scr_manager.current = 'add_customer_screen'
        self.clear_selected_items()

    def on_customers_edit_button_clicked(self, *args):
        edit_customer_screen = App.get_running_app().root.ids.scr_manager.get_screen('edit_customer_screen')
        edit_customer_screen.customer_id = self.ids.customers_view.selected_item.customer_id
        App.get_running_app().root.ids.scr_manager.current = 'edit_customer_screen'
        self.clear_selected_items()

    def on_customers_delete_button_clicked(self, *args):
        selected_customer_id = self.ids.customers_view.selected_item.customer_id
        self.clear_selected_items()
        local_storage.erase_customer_info(selected_customer_id)
        self.ids.customers_view.populate()
