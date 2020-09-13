kv = """
<AddCustomerScreen@Screen>:
    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'bottom'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .08
            padding: 10
            spacing: 2
            Button:
                id: buy_save_customer_button
                text: "Save Customer"
                width: 120
                size_hint_x: None
                on_release: root.on_add_customer_save_button_clicked()
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
                text: "First name:"
            TextInput:
                id: customer_first_name_input
                text: "John"
            Label:
                text: "Last name:"
            TextInput:
                id: customer_last_name_input
                text: "Smith"
            Label:
                text: "Face:"
            Button:
                id: customer_face_photo_button
                text: "take picture"
            Label:
                text: "Passport / ID:"
            Button:
                id: customer_passport_photo_button
                text: "take picture"
"""