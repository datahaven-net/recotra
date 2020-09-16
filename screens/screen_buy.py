kv = """
<BuyScreen@Screen>:
    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'bottom'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .08
            padding: 10
            spacing: 2
            RoundedButton:
                id: buy_save_customer_button
                text: "Select Customer"
                width: 120
                size_hint_x: None
                # on_release: root.on_buy_select_customer_button_clicked()
            RoundedButton:
                text: "PDF file"
                width: 120
                size_hint_x: None
                # on_release: root.on_buy_pdf_file_button_clicked()
            RoundedButton: 
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
                text: "Seller:"
            TextInput:
                id: buy_person_name_input
                text: "John Smith"
            Label:
                text: "BTC price (US $ / BTC):"
            TextInput:
                id: buy_btc_price_input
                text: "10200"
            Label:
                text: "Amount (US $):"
            TextInput:
                id: buy_usd_amount_input
                text: "1000"
            Label:
                text: "Receiving BitCoin address:"
            TextInput:
                id: buy_receive_address_input
                text: "1FiTczw1GeaEdMoGbQWngWT8gCirYuzfne"

"""
