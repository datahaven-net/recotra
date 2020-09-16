from kivy.properties import BooleanProperty, ObjectProperty  # @UnresolvedImport
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.stacklayout import StackLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.views import _cached_views, _view_base_cache
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
        print('SelectableRecord.apply_selection', index, self.selected, is_selected)
        if is_selected:
            rv.selected_item = self
        else:
            rv.selected_item = None
        self.selected = is_selected


class SelectableRecycleView(RecycleView):

    selected_item = ObjectProperty(None, allownone=True)

    def clear_selection(self):
        print('clear_selection', self.selected_item)
        if self.selected_item:
            print(self.selected_item.selected)
            self.selected_item.selected = False
            self.selected_item = None
