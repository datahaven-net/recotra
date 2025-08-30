from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty  # @UnresolvedImport


kv = """
<BTCAddressDialog>:
    title: 'change BTC address'
    size_hint: None, None
    size: 500, 130
    auto_dismiss: True
    text: input.text

    BoxLayout:
        orientation: 'vertical'
        pos: self.pos
        size: root.size

        BoxLayout:
            orientation: 'horizontal'
            TextInput:
                id: input
                multiline: False
                hint_text: ''

        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'save'
                background_color: 0,255,0,0.7
                on_press: root._enter()

            Button:
                text: 'cancel'
                background_color: 128,128,128,0.7
                on_press: root._cancel()


<InputTextMultilineContent>:
    orientation: "vertical"
    spacing: dp(12)
    size_hint: (1, 1)

    TextInput:
        id: text_input
        multiline: True
        text: ''
        halign: 'left'
        text_size: self.size
        size_hint: 1, 1
"""

#------------------------------------------------------------------------------

class BTCAddressDialog(Popup):

    def __init__(self, btc_address, callback, *args, **kwargs):
        super(BTCAddressDialog, self).__init__(*args, **kwargs)
        self.callback = callback
        self.ids.input.text = btc_address

    def _enter(self):
        if self.text:
            self.dismiss()
            self.callback(self.text)

    def _cancel(self):
        self.dismiss()

#------------------------------------------------------------------------------

def show_one_button_dialog(title, message, dialog_size=(dp(400), dp(200), ), button_text='close'):
    layout = BoxLayout(
        orientation='vertical',
        padding=dp(5),
    )
    popupLabel = Label(
        text=message,
        text_size=(dialog_size[0]-dp(20), None, ),
        height=dialog_size[1]-dp(50),
        size_hint=(1, None, ),
        color=(1, 1, 1, 1, ),
        valign='top',
        halign='center',
    )
    closeButton = Button(
        text=button_text,
        size_hint=(None, None, ),
        size=(dp(45), dp(20), ),
        pos_hint={'right': 1},
    )
    layout.add_widget(popupLabel)
    layout.add_widget(closeButton)
    popup = Popup(
        title=title,
        title_align='center',
        content=layout,
        size_hint=(None, None, ),
        size=dialog_size,
    )
    popup.open()
    closeButton.bind(on_press=popup.dismiss)

#------------------------------------------------------------------------------

class InputTextMultilineContent(BoxLayout):
    pass

#------------------------------------------------------------------------------

def open_text_input_dialog(title, text, dialog_size=(dp(400), dp(200), ), button_confirm='Confirm', button_cancel='Cancel', cb=None):
    layout = BoxLayout(orientation='vertical', padding=dp(3))
    content = InputTextMultilineContent()
    content.ids.text_input.text = text
    layout.add_widget(content)
    if button_confirm:
        confirm_button = Button(
            color=(1,1,1,1),
            text=button_confirm,
            size_hint=(None, None, ),
            size=(dp(70), dp(25), ),
            pos_hint={'right': 1},
        )
        layout.add_widget(confirm_button)
    if button_cancel:
        close_button = Button(
            color=(1,1,1,1),
            text=button_cancel,
            size_hint=(None, None, ),
            size=(dp(70), dp(25), ),
            pos_hint={'right': 1},
        )
        layout.add_widget(close_button)
    popup = Popup(
        title=title,
        title_align='center',
        title_color=(0,0,0,1),
        background='',
        content=layout,
        size_hint=(None, None, ),
        size=dialog_size,
    )

    def on_close(*args, **kwargs):
        popup.dismiss()
        if cb:
            cb(None)

    def on_confirm(*args, **kwargs):
        inp = content.ids.text_input.text
        popup.dismiss()
        if cb:
            cb(inp)

    def on_open(*args, **kwargs):
        content.ids.text_input.focus = True

    confirm_button.bind(on_press=on_confirm)
    close_button.bind(on_press=on_close)
    popup.bind(on_open=on_open)
    popup.open()
    return popup
