from kivy.uix.textinput import TextInput

#------------------------------------------------------------------------------

from components.screen import AppScreen
from storage import local_storage
from lib import btc_util

#------------------------------------------------------------------------------

kv = """
<OptionHeaderLabel@Label>:
    size_hint_x: None
    size_hint_y: None
    width: dp(280)
    height: dp(50)
    valign: 'bottom'
    halign: 'right'
    pos_hint: {'right': 1}
    text_size: self.size
    font_size: sp(18)


<OptionFieldLabel@Label>:
    size_hint_x: None
    size_hint_y: None
    width: dp(280)
    height: dp(30)
    pos_hint: {'right': 1}
    valign: 'middle'
    halign: 'right'
    text_size: self.size


<OptionFieldInput@TextInput>:
    size_hint_x: None
    size_hint_y: None
    width: dp(380)
    height: self.minimum_height
    multiline: False


<OptionFieldMultilineInput@TextInput>:
    size_hint_x: None
    size_hint_y: None
    width: dp(380)
    height: dp(50)
    multiline: True


<OptionFieldBTCAddressListInput>:
    size_hint_x: None
    size_hint_y: None
    width: dp(380)
    height: dp(100)
    multiline: True


<SettingsScreen>:

    BoxLayout:
        orientation: 'vertical'
        size_hint: 1, 1

        ScrollView:
            bar_width: dp(15)
            bar_color: .2,.5,.8,1
            bar_inactive_color: .1,.4,.7,1
            effect_cls: "ScrollEffect"
            scroll_type: ['bars']

            BoxLayout:
                orientation: 'horizontal'
                size_hint: 1, None
                height: self.minimum_height

                Widget:
                    size: 1, 1
                    size_hint: 0.5, 1

                GridLayout:
                    size_hint_x: None
                    size_hint_y: None
                    width: self.minimum_width
                    height: self.minimum_height
                    pos_hint: {'center_x': 0.5, 'top': 1}
                    cols: 2
                    padding: dp(10)
                    spacing: dp(10)

                    OptionHeaderLabel:
                        text: "company business details"
                    Widget:
                        size: 1, 1

                    OptionFieldLabel:
                        text: "company name:"
                    OptionFieldInput:
                        id: business_company_name
                        text: ""
                        on_text: root.on_field_modified('business_company_name')

                    OptionFieldLabel:
                        text: "owner first name:"
                    OptionFieldInput:
                        id: business_owner_first_name
                        text: ""
                        on_text: root.on_field_modified('business_owner_first_name')

                    OptionFieldLabel:
                        text: "owner last name:"
                    OptionFieldInput:
                        id: business_owner_last_name
                        text: ""
                        on_text: root.on_field_modified('business_owner_last_name')

                    OptionFieldLabel:
                        text: "address:"
                    OptionFieldInput:
                        id: business_address
                        text: ""
                        on_text: root.on_field_modified('business_address')

                    OptionFieldLabel:
                        text: "email:"
                    OptionFieldInput:
                        id: business_email
                        text: ""
                        on_text: root.on_field_modified('business_email')

                    OptionFieldLabel:
                        text: "phone number:"
                    OptionFieldInput:
                        id: business_phone
                        text: ""
                        on_text: root.on_field_modified('business_phone')

                    OptionFieldLabel:
                        text: "receiving BitCoin addresses:"
                    OptionFieldBTCAddressListInput:
                        id: receiving_btc_address
                        text: ""
                        on_text: root.on_field_modified('receiving_btc_address')

                    OptionFieldLabel:
                        text: "disclosure statement:"
                    OptionFieldMultilineInput:
                        id: disclosure_statement
                        text: ""
                        on_text: root.on_field_modified('disclosure_statement')

                    OptionHeaderLabel:
                        text: "access to live BTC/USD prices"
                    Widget:
                        size: 1, 1

                    OptionFieldLabel:
                        text: "CoinMarketCap API key:"
                    OptionFieldInput:
                        id: coinmarketcap_api_key
                        text: ""
                        on_text: root.on_field_modified('coinmarketcap_api_key')

                    OptionHeaderLabel:
                        text: "buy/sell commission percent"
                    Widget:
                        size: 1, 1

                    OptionFieldLabel:
                        text: "price offset when customer buying BTC:"
                    OptionFieldInput:
                        id: btc_usd_commission_percent
                        hint_text: '2.5'
                        text: ""
                        on_text: root.on_field_modified('btc_usd_commission_percent')

                    OptionFieldLabel:
                        text: "price offset when customer selling BTC:"
                    OptionFieldInput:
                        id: usd_btc_commission_percent
                        hint_text: '2.5'
                        text: ""
                        on_text: root.on_field_modified('usd_btc_commission_percent')

                    OptionHeaderLabel:
                        text: "contracts verification against live Blockchain"
                    Widget:
                        size: 1, 1

                    OptionFieldLabel:
                        text: "price precision matching percent:"
                    OptionFieldInput:
                        id: price_precision_matching_percent
                        hint_text: '2.0'
                        text: ""
                        on_text: root.on_field_modified('price_precision_matching_percent')

                    OptionFieldLabel:
                        text: "price precision fixed amount ($ US):"
                    OptionFieldInput:
                        id: price_precision_fixed_amount
                        hint_text: '25'
                        text: ""
                        on_text: root.on_field_modified('price_precision_fixed_amount')

                    OptionFieldLabel:
                        text: "time offset - seconds before:"
                    OptionFieldInput:
                        id: time_matching_seconds_before
                        hint_text: '3600'
                        text: ""
                        on_text: root.on_field_modified('time_matching_seconds_before')

                    OptionFieldLabel:
                        text: "time offset - seconds after:"
                    OptionFieldInput:
                        id: time_matching_seconds_after
                        hint_text: '21600'
                        text: ""
                        on_text: root.on_field_modified('time_matching_seconds_after')

                    OptionFieldLabel:
                        text: "skip contracts older than number of days:"
                    OptionFieldInput:
                        id: contract_expiration_period_days
                        hint_text: '90'
                        text: ""
                        on_text: root.on_field_modified('contract_expiration_period_days')

                    OptionHeaderLabel:
                        text: "paper contracts"
                    Widget:
                        size: 1, 1

                    OptionFieldLabel:
                        text: "QR code size (pixels)"
                    OptionFieldInput:
                        id: qr_code_size
                        text: ""
                        on_text: root.on_field_modified('qr_code_size')

                Widget:
                    size: 1, 1
                    size_hint: 0.5, 1

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, None
            padding: dp(10)
            spacing: dp(2)

            RoundedButton:
                id: save_settings_button
                size_hint_x: None
                width: dp(120)
                text: ' save '
                disabled: True
                on_release: root.on_save_button_clicked()

"""

#------------------------------------------------------------------------------

class OptionFieldBTCAddressListInput(TextInput):

    def insert_text(self, substring, from_undo=False):
        if substring.count('\n') == 0: 
            return super().insert_text(substring, from_undo)
        if substring.count('\n') == 1 and len(substring) == 1:
            return super().insert_text(substring, from_undo)
        newsubstring = ''
        for line in substring.split('\n'):
            words = line.split()
            btc_address = ''
            for word in words:
                if btc_util.validate_btc_address(word):
                    btc_address = word
                    break
            if not btc_address:
                continue
            newsubstring += btc_address + '\n'
        return super().insert_text(newsubstring, from_undo)


class SettingsScreen(AppScreen):

    def populate(self, *args):
        cur_settings = local_storage.read_settings()
        self.ids.business_company_name.text = cur_settings.get('business_company_name', '')
        self.ids.business_owner_first_name.text = cur_settings.get('business_owner_first_name', '')
        self.ids.business_owner_last_name.text = cur_settings.get('business_owner_last_name', '')
        self.ids.business_address.text = cur_settings.get('business_address', '')
        self.ids.business_email.text = cur_settings.get('business_email', '')
        self.ids.business_phone.text = cur_settings.get('business_phone', '')
        self.ids.disclosure_statement.text = cur_settings.get('disclosure_statement', '')
        self.ids.receiving_btc_address.text = '\n'.join(cur_settings.get('receiving_btc_address_list', []))
        self.ids.coinmarketcap_api_key.text = cur_settings.get('coinmarketcap_api_key', '')
        self.ids.btc_usd_commission_percent.text = cur_settings.get('btc_usd_commission_percent', '0.0')
        self.ids.usd_btc_commission_percent.text = cur_settings.get('usd_btc_commission_percent', '0.0')
        self.ids.price_precision_matching_percent.text = cur_settings.get('price_precision_matching_percent', '1.0')
        self.ids.price_precision_fixed_amount.text = cur_settings.get('price_precision_fixed_amount', '1.0')
        self.ids.time_matching_seconds_before.text = cur_settings.get('time_matching_seconds_before', '0')
        self.ids.time_matching_seconds_after.text = cur_settings.get('time_matching_seconds_after', '0')
        self.ids.contract_expiration_period_days.text = cur_settings.get('contract_expiration_period_days', '0')
        self.ids.qr_code_size.text = cur_settings.get('qr_code_size', '600')
        self.ids.save_settings_button.disabled = True

    def on_enter(self, *args):
        self.populate()

    def on_field_modified(self, field_name):
        self.ids.save_settings_button.disabled = False

    def on_save_button_clicked(self, *args):
        cur_settings = local_storage.read_settings()
        cur_settings['business_company_name'] = self.ids.business_company_name.text
        cur_settings['business_owner_first_name'] = self.ids.business_owner_first_name.text
        cur_settings['business_owner_last_name'] = self.ids.business_owner_last_name.text
        cur_settings['business_address'] = self.ids.business_address.text
        cur_settings['business_email'] = self.ids.business_email.text
        cur_settings['business_phone'] = self.ids.business_phone.text
        cur_settings['disclosure_statement'] = self.ids.disclosure_statement.text
        cur_settings['receiving_btc_address_list'] = list(filter(None, self.ids.receiving_btc_address.text.split('\n')))
        cur_settings['coinmarketcap_api_key'] = self.ids.coinmarketcap_api_key.text
        cur_settings['btc_usd_commission_percent'] = self.ids.btc_usd_commission_percent.text
        cur_settings['usd_btc_commission_percent'] = self.ids.usd_btc_commission_percent.text
        cur_settings['price_precision_matching_percent'] = self.ids.price_precision_matching_percent.text
        cur_settings['price_precision_fixed_amount'] = self.ids.price_precision_fixed_amount.text
        cur_settings['time_matching_seconds_before'] = self.ids.time_matching_seconds_before.text
        cur_settings['time_matching_seconds_after'] = self.ids.time_matching_seconds_after.text
        cur_settings['contract_expiration_period_days'] = self.ids.contract_expiration_period_days.text
        cur_settings['qr_code_size'] = self.ids.qr_code_size.text
        local_storage.write_settings(cur_settings)
        self.ids.save_settings_button.disabled = True
