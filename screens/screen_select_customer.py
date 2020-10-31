from kivy.app import App
from kivy.properties import ObjectProperty  # @UnresolvedImport

#------------------------------------------------------------------------------

from components.screen import AppScreen
from components.list_view import SelectableRecycleView
from storage import local_storage

#------------------------------------------------------------------------------

kv = """
<SelectCustomerRecord@SelectableRecord>:
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

<SelectCustomerView>:
    viewclass: 'SelectCustomerRecord'

    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: False

<SelectCustomerScreen>:
    customer_select_button: customer_select_button
    BoxLayout:
        orientation: 'vertical'
        SelectCustomerView:
            id: select_customer_view
            size_hint: 1, 1
        BoxLayout:
            orientation: 'horizontal'
            size_hint: None, None
            height: self.minimum_height
            padding: 10
            spacing: 2
            RoundedButton:
                id: customer_select_button
                text: 'select'
                width: 120
                size_hint_x: None
                disabled: True
                on_press: root.on_customer_select_button_clicked()
"""

#------------------------------------------------------------------------------

class SelectCustomerView(SelectableRecycleView):

    def __init__(self, **kwargs):
        super(SelectCustomerView, self).__init__(**kwargs)
        self.populate()

    def populate(self):
        self.data = []
        for customer_info in local_storage.make_customers_ui_data(
                customers_list=local_storage.load_customers_list(sort_by='customer_id'),
            ):
            self.data.append(customer_info)

    def on_selection_applied(self, item, index, is_selected, prev_selected):
        select_cust_screen = App.get_running_app().root.ids.scr_manager.get_screen('select_customer_screen')
        select_cust_screen.customer_select_button.disabled = not is_selected

#------------------------------------------------------------------------------

class SelectCustomerScreen(AppScreen):

    customer_select_button = ObjectProperty(None, allownone=True)
    customer_selected_callback = None

    def on_pre_enter(self, *args):
        self.ids.select_customer_view.populate()

    def clear_selected_items(self):
        self.ids.select_customer_view.clear_selection()
        self.ids.customer_select_button.disabled = True

    def on_leave(self, *args):
        self.clear_selected_items()

    def on_customer_select_button_clicked(self):
        selected_customer_id = self.ids.select_customer_view.selected_item.customer_id
        if self.customer_selected_callback:
            self.customer_selected_callback(selected_customer_id)
            self.customer_selected_callback = None
