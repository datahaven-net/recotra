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
    height: dp(70)
    size_hint_y: None
    customer_id: 'customer_id'
    first_name: 'first_name'
    last_name: 'last_name'
    Label:
        id: customer_id
        text: root.customer_id
        size_hint: None, 0.5
        width: dp(40)
    Label:
        id: first_name
        text: root.first_name
        bold: True
        size_hint: None, 0.5
        width: self.texture_size[0] + dp(10)
    Label:
        id: last_name
        text: root.last_name
        size_hint: None, 0.5
        width: self.texture_size[0] + dp(10)

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

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, None
            height: self.minimum_height
            padding: dp(10)
            spacing: dp(2)

            Widget:

            TextInput:
                id: search_input
                text: ""
                right: self.width
                width: dp(120)
                height: dp(30)
                size_hint_x: None
                size_hint_y: None
                on_text: root.on_search_button_text_changed()

            RoundedButton:
                size_hint: None, None
                width: dp(30)
                height: dp(30)
                text: fa_icon('search')
                on_press: root.on_search_button_clicked()

        SelectCustomerView:
            id: select_customer_view
            size_hint: 1, 1

        BoxLayout:
            orientation: 'horizontal'
            size_hint: None, None
            height: self.minimum_height
            padding: dp(10)
            spacing: dp(2)

            RoundedButton:
                id: customer_select_button
                text: 'select'
                width: dp(120)
                size_hint_x: None
                disabled: True
                on_press: root.on_customer_select_button_clicked()
"""

#------------------------------------------------------------------------------

class SelectCustomerView(SelectableRecycleView):

    def __init__(self, **kwargs):
        super(SelectCustomerView, self).__init__(**kwargs)
        self.data_copy = []
        self.populate()

    def populate(self):
        self.data = []
        for customer_info in local_storage.make_customers_ui_data(local_storage.load_customers_list(sort_by='customer_id')):
            self.data.append(customer_info)
        self.data_copy = list(self.data)

    def on_selection_applied(self, item, index, is_selected, prev_selected):
        select_cust_screen = App.get_running_app().root.ids.scr_manager.get_screen('select_customer_screen')
        select_cust_screen.customer_select_button.disabled = not is_selected

#------------------------------------------------------------------------------

class SelectCustomerScreen(AppScreen):

    customer_select_button = ObjectProperty(None, allownone=True)
    customer_selected_callback = None

    def clear_selected_items(self):
        self.ids.select_customer_view.clear_selection()
        self.ids.customer_select_button.disabled = True

    def populate_search_results(self):
        s = self.ids.search_input.text.lower()
        new_data = []
        if s:
            for d in self.ids.select_customer_view.data_copy:
                matched = False
                if d['first_name'].lower().count(s) or d['last_name'].lower().count(s):
                    matched = True
                if str(d['customer_id']).count(s):
                    matched = True
                if matched:
                    new_data.append(d)
        else:
            new_data = list(self.ids.select_customer_view.data_copy)
        self.ids.select_customer_view.data = new_data

    def on_enter(self, *args):
        self.ids.select_customer_view.populate()

    def on_leave(self, *args):
        self.clear_selected_items()

    def on_customer_select_button_clicked(self):
        selected_customer_id = self.ids.select_customer_view.selected_item.customer_id
        if self.customer_selected_callback:
            self.customer_selected_callback(selected_customer_id)
            self.customer_selected_callback = None

    def on_search_button_clicked(self, *args):
        self.populate_search_results()

    def on_search_button_text_changed(self, *args):
        self.populate_search_results()
