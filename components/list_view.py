from kivy.properties import BooleanProperty  # @UnresolvedImport
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.stacklayout import StackLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout

#------------------------------------------------------------------------------

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):

    touch_deselect_last = BooleanProperty(True)


class SelectableRecord(RecycleDataViewBehavior, StackLayout):

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableRecord, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableRecord, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
