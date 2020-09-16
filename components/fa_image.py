from kivy.properties import StringProperty, ColorProperty, NumericProperty  # @UnresolvedImport

from kivy.core.text import Label as CoreLabel
from kivy.core.text.markup import MarkupLabel as CoreMarkupLabel
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

from components.webfont import fa_icon


class FaImage(Image):

    fa_name = StringProperty('smile')
    fa_icon_color = ColorProperty((0, 1, 0, 1))
    fa_font_size = NumericProperty(12)

    def __init__(self, **kwargs):
        self.fa_name = kwargs.get('fa_name', 'smile')
        self.fa_icon_color = kwargs.get('fa_icon_color', (0, 1, 0, 1))
        self.fa_font_size = kwargs.get('fa_font_size', 12)
        super(FaImage, self).__init__(**kwargs)

    
    def render(self):
        mylabel = CoreMarkupLabel(text=fa_icon(self.fa_name), font_size=self.fa_font_size, color=self.fa_icon_color)
        mylabel.refresh()
        texture = mylabel.texture
        texture_size = list(texture.size)
        self.canvas.add(Rectangle(texture=texture, size=texture_size))
