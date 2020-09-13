kv = """
<SellScreen@Screen>:
    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'bottom'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .08
            padding: 10
            spacing: 2
            Button:
                id: sell_save_customer_button
                text: "Save Customer"
                width: 120
                size_hint_x: None
                on_release: root.on_sell_save_customer_button_clicked()
            Button:
                text: "PDF file"
                width: 120
                size_hint_x: None
            Button: 
                text: "Print"
                width: 120
                size_hint_x: None
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        GridLayout:
            cols: 2
            padding: 10
            spacing: 2
            row_force_default: True
            row_default_height: 40
            Label:
                text: "Buyer:"
            TextInput: 
                text: "John Smith"
            Label:
                text: "BTC price (US $ / BTC):"
            TextInput: 
                text: "10200"
            Label:
                text: "Amount (US $):"
            TextInput: 
                text: "1000"
            Label:
                text: "Destination BitCoin address:"
            TextInput: 
                text: "1FiTczw1GeaEdMoGbQWngWT8gCirYuzfne"
"""