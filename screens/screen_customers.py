from kivy.app import App
from kivy.properties import ObjectProperty  # @UnresolvedImport

#------------------------------------------------------------------------------

from components.screen import AppScreen
from components.list_view import SelectableRecycleView
from components.webfont import fa_icon
from storage import local_storage

#------------------------------------------------------------------------------

_Debug = False

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

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, None
            height: self.minimum_height
            padding: dp(10)
            spacing: dp(2)

            RoundedButton:
                id: sort_by_id_button
                size_hint: None, None
                width: self.texture_size[0] + dp(20)
                height: dp(30)
                text: 'ID ' + fa_icon('sort-numeric-down')
                on_press: root.on_sort_by_id_button_clicked()

            RoundedButton:
                id: sort_by_name_button
                size_hint: None, None
                width: self.texture_size[0] + dp(20)
                height: dp(30)
                text: 'First Name ' + fa_icon('')
                on_press: root.on_sort_by_name_button_clicked()

            RoundedButton:
                id: sort_by_last_name_button
                size_hint: None, None
                width: self.texture_size[0] + dp(20)
                height: dp(30)
                text: 'Last Name ' + fa_icon('')
                on_press: root.on_sort_by_last_name_button_clicked()

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

        CustomersView:
            id: customers_view
            size_hint: 1, 1

        BoxLayout:
            orientation: 'horizontal'
            size_hint: None, None
            height: self.minimum_height
            padding: dp(10)
            spacing: dp(2)

            RoundedButton:
                id: customer_add_button
                text: 'add'
                width: dp(120)
                size_hint_x: None
                on_press: root.on_customers_add_button_clicked()

            RoundedButton:
                id: customer_edit_button
                text: 'modify'
                width: dp(120)
                size_hint_x: None
                disabled: True
                on_press: root.on_customers_edit_button_clicked()

            RoundedButton:
                id: customer_delete_button
                text: 'erase'
                width: dp(120)
                size_hint_x: None
                disabled: True
                on_press: root.on_customers_delete_button_clicked()
"""

#------------------------------------------------------------------------------

class CustomersView(SelectableRecycleView):

    def __init__(self, **kwargs):
        super(CustomersView, self).__init__(**kwargs)
        self.data_copy = []
        self.populate()

    def populate(self):
        self.data = []
        for customer_info in local_storage.make_customers_ui_data(local_storage.load_customers_list(sort_by='customer_id')):
            self.data.append(customer_info)
        self.data_copy = list(self.data)

    def on_selection_applied(self, item, index, is_selected, prev_selected):
        if _Debug:
            print('on_selection_applied', item, index, is_selected, prev_selected)
        cust_screen =  App.get_running_app().root.ids.scr_manager.get_screen('customers_screen')
        cust_screen.customer_delete_button.disabled = not is_selected
        cust_screen.customer_edit_button.disabled = not is_selected

#------------------------------------------------------------------------------

class CustomersScreen(AppScreen):

    customer_edit_button = ObjectProperty(None, allownone=True)
    customer_delete_button = ObjectProperty(None, allownone=True)
    sort_by = 'customer_id_down'

    def clear_selected_items(self):
        if _Debug:
            print('clear_selected_items')
        self.ids.customers_view.clear_selection()
        self.ids.customer_edit_button.disabled = True
        self.ids.customer_delete_button.disabled = True

    def enable_action_buttons(self):
        if _Debug:
            print('enable_action_buttons')
        self.ids.customer_edit_button.disabled = False
        self.ids.customer_delete_button.disabled = False

    def populate_search_results(self):
        s = self.ids.search_input.text.lower()
        new_data = []
        if s:
            for d in self.ids.customers_view.data_copy:
                matched = False
                if d['first_name'].lower().count(s) or d['last_name'].lower().count(s):
                    matched = True
                if str(d['customer_id']).count(s):
                    matched = True
                if matched:
                    new_data.append(d)
        else:
            new_data = list(self.ids.customers_view.data_copy)
        if self.sort_by == 'customer_id_down':
            new_data.sort(key=lambda d: int(d['customer_id']), reverse=False)
        elif self.sort_by == 'customer_id_up':
            new_data.sort(key=lambda d: int(d['customer_id']), reverse=True)
        elif self.sort_by == 'name_down':
            new_data.sort(key=lambda d: d['first_name'].lower(), reverse=False)
        elif self.sort_by == 'name_up':
            new_data.sort(key=lambda d: d['first_name'].lower(), reverse=True)
        elif self.sort_by == 'last_name_down':
            new_data.sort(key=lambda d: d['last_name'].lower(), reverse=False)
        elif self.sort_by == 'last_name_up':
            new_data.sort(key=lambda d: d['last_name'].lower(), reverse=True)
        self.ids.customers_view.data = new_data

    def on_enter(self, *args):
        if _Debug:
            print('on_enter', self.ids.customers_view.selected_item)
        if self.ids.customers_view.selected_item:
            self.enable_action_buttons()

    def on_leave(self, *args):
        self.clear_selected_items()

    def on_customers_add_button_clicked(self, *args):
        add_customer_screen = self.scr_manager().get_screen('add_customer_screen')
        add_customer_screen.new_customer_id = None
        self.scr_manager().current = 'add_customer_screen'
        self.clear_selected_items()

    def on_customers_edit_button_clicked(self, *args):
        edit_customer_screen = App.get_running_app().root.ids.scr_manager.get_screen('edit_customer_screen')
        edit_customer_screen.customer_id = self.ids.customers_view.selected_item.customer_id
        self.scr_manager().current = 'edit_customer_screen'
        self.clear_selected_items()

    def on_customers_delete_button_clicked(self, *args):
        selected_customer_id = self.ids.customers_view.selected_item.customer_id
        self.clear_selected_items()
        local_storage.erase_customer_info(selected_customer_id)
        self.ids.customers_view.populate()

    def on_search_button_clicked(self, *args):
        self.populate_search_results()

    def on_search_button_text_changed(self, *args):
        self.populate_search_results()

    def on_sort_by_id_button_clicked(self, *args):
        self.ids.sort_by_id_button.text = 'ID ' + fa_icon('')
        self.ids.sort_by_name_button.text = 'First Name ' + fa_icon('')
        self.ids.sort_by_last_name_button.text = 'Last Name ' + fa_icon('')
        if self.sort_by == 'customer_id_down':
            self.sort_by = 'customer_id_up'
            self.ids.sort_by_id_button.text = 'ID ' + fa_icon('sort-numeric-up')
        elif self.sort_by == 'customer_id_up':
            self.sort_by = 'customer_id_down'
            self.ids.sort_by_id_button.text = 'ID ' + fa_icon('sort-numeric-down')
        else:
            self.sort_by = 'customer_id_down'
            self.ids.sort_by_id_button.text = 'ID ' + fa_icon('sort-numeric-down')
        self.populate_search_results()

    def on_sort_by_name_button_clicked(self, *args):
        self.ids.sort_by_id_button.text = 'ID ' + fa_icon('')
        self.ids.sort_by_name_button.text = 'First Name ' + fa_icon('')
        self.ids.sort_by_last_name_button.text = 'Last Name ' + fa_icon('')
        if self.sort_by == 'name_down':
            self.sort_by = 'name_up'
            self.ids.sort_by_name_button.text = 'First Name ' + fa_icon('sort-alpha-up')
        elif self.sort_by == 'name_up':
            self.sort_by = 'name_down'
            self.ids.sort_by_name_button.text = 'First Name ' + fa_icon('sort-alpha-down')
        else:
            self.sort_by = 'name_down'
            self.ids.sort_by_name_button.text = 'First Name ' + fa_icon('sort-alpha-down')
        self.populate_search_results()

    def on_sort_by_last_name_button_clicked(self, *args):
        self.ids.sort_by_id_button.text = 'ID ' + fa_icon('')
        self.ids.sort_by_name_button.text = 'First Name ' + fa_icon('')
        self.ids.sort_by_last_name_button.text = 'Last Name ' + fa_icon('')
        if self.sort_by == 'last_name_down':
            self.sort_by = 'last_name_up'
            self.ids.sort_by_last_name_button.text = 'Last Name ' + fa_icon('sort-alpha-up')
        elif self.sort_by == 'last_name_up':
            self.sort_by = 'last_name_down'
            self.ids.sort_by_last_name_button.text = 'Last Name ' + fa_icon('sort-alpha-down')
        else:
            self.sort_by = 'last_name_down'
            self.ids.sort_by_last_name_button.text = 'Last Name ' + fa_icon('sort-alpha-down')
        self.populate_search_results()
