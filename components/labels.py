kv = """
<Label>:
    markup: True
    color: 0, 0, 0, 1


<RightAlignLabel@Label>:
    text_size: self.size
    halign: 'right'
    padding_x: 10


<LeftAlignLabel@Label>:
    text_size: self.size
    halign: 'left'
    padding_x: 10


<TopAlignLabel@Label>:
    text_size: self.size
    valign: 'top'
    padding_y: 10


<BottomAlignLabel@Label>:
    text_size: self.size
    valign: 'bottom'
    padding_y: 10

"""
