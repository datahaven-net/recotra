from kivy.app import App
from kivy.properties import ObjectProperty  # @UnresolvedImport

#------------------------------------------------------------------------------

from components.screen import AppScreen
from storage import local_storage

#------------------------------------------------------------------------------

kv = """
<OptionFieldLabel@RightAlignLabel>:
    size_hint_x: None
    width: dp(200)
    valign: 'middle'


<OptionFieldInput@TextInput>:
    size_hint_x: None
    size_hint_y: None
    width: dp(360)
    height: self.minimum_height
    multiline: False


<SettingsScreen>:

    BoxLayout:
        orientation: 'vertical'
        size_hint: 1, 1

        ScrollView:
            bar_width: 15
            bar_color: .2,.5,.8,1
            bar_inactive_color: .1,.4,.7,1
            effect_cls: "ScrollEffect"
            scroll_type: ['bars']

            GridLayout:
                size_hint_y: None
                height: self.minimum_height
                cols: 2
                padding: 10
                spacing: 10

                OptionFieldLabel:
                    text: "receiving BitCoin address:"
                OptionFieldInput:
                    id: receiving_btc_address
                    text: ""
                    on_text: root.on_field_modified('receiving_btc_address')

                OptionFieldLabel:
                    text: "CoinMarketCap API key:"
                OptionFieldInput:
                    id: coinmarketcap_api_key
                    text: ""
                    on_text: root.on_field_modified('coinmarketcap_api_key')

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, None
            padding: 10
            spacing: 2

            RoundedButton:
                id: save_settings_button
                size_hint_x: None
                width: 120
                text: ' save '
                disabled: True
                on_release: root.on_save_button_clicked()

"""

#------------------------------------------------------------------------------

class SettingsScreen(AppScreen):

    def populate(self, *args):
        cur_settings = local_storage.read_settings()
        self.ids.receiving_btc_address.text = cur_settings.get('receiving_btc_address', '')
        self.ids.coinmarketcap_api_key.text = cur_settings.get('coinmarketcap_api_key', '')
        self.ids.save_settings_button.disabled = True

    def on_enter(self, *args):
        self.populate()

    def on_field_modified(self, field_name):
        self.ids.save_settings_button.disabled = False

    def on_save_button_clicked(self, *args):
        cur_settings = local_storage.read_settings()
        cur_settings['receiving_btc_address'] = self.ids.receiving_btc_address.text
        cur_settings['coinmarketcap_api_key'] = self.ids.coinmarketcap_api_key.text
        local_storage.write_settings(cur_settings)
