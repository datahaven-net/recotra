from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout


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
