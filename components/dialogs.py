from kivy.uix.popup import Popup


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
