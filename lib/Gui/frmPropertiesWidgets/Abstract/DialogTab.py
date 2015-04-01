import gtk
from lib.Gui.frmPropertiesWidgets import CEditableComboBox, CEditBoxWithButton, CEditBox, CComboBox, CTextArea, CTable


class CDialogTab(object):
    def __init__(self):
        self.frame = gtk.Frame()
        self.items = {}

        self.__vbox = gtk.VBox(False)
        self.frame.add(self.__vbox)

        self.__table = gtk.Table(0, 2)
        self.__table.set_col_spacings(5)
        self.__table.set_row_spacings(1)
        self.__vbox.pack_start(self.__table, False, False, 0)

        self.__vpaned = gtk.VPaned()
        self.__vbox.pack_start(self.__vpaned)

        self.frame.show_all()

        self.__table_item_manager = CDialogTab.CTableItemManager(self.__table)
        self.__other_item_manager = CDialogTab.COtherItemManager(self.__vbox, self.__vpaned)

    def GetFrame(self):
        return self.frame

    def GetItemCount(self):
        return len(self.items)

    def RemoveItem(self, itemid):
        if itemid not in self.items:
            raise KeyError("Item with id {0} doesn't exist in CDialogTab.".format(itemid))

        item = self.items[itemid]

        if isinstance(item, CDialogTab.CTableRowItem):
            self.__table_item_manager.RemoveItem(item)
        elif isinstance(item, CDialogTab.COtherItem):
            del self.items[itemid]
            self.__other_item_manager.RemoveItem(item)


    def AppendItem(self, itemid, item, itemname):
        if itemid in self.items:
            raise KeyError("Item with id {0} already exists".format(itemid))

        if isinstance(item, CComboBox) or isinstance(item, CEditableComboBox) or \
                isinstance(item, CEditBox) or isinstance(item, CEditBoxWithButton):
            row_item =  CDialogTab.CTableRowItem(itemid, item, itemname)
            self.items[itemid] = row_item
            self.__table_item_manager.AppendItem(row_item)
        elif isinstance(item, (CTable, CTextArea)):
            other_item = CDialogTab.COtherItem(itemid, item, itemname)
            self.items[itemid] = other_item
            self.__InsertOtherItem(other_item)

    def __InsertOtherItem(self, item):
        self.__other_item_manager.AddItem(item)

    def __RemoveOtherItem(self, itemid):
        item = self.items[itemid]
        del self.items[itemid]

        self.__other_item_manager.RemoveItem(item)

    class CTableItemManager(object):
        def __init__(self, table):
            self.__table = table
            self.__items = {}
            self.__items_order = []

        def GetItemCount(self):
            return len(self.__items)

        def RemoveItem(self, row_item):
            for i, itemid in enumerate(self.__items_order):
                if itemid == row_item.GetItemId():
                    row = i
                    break
            else:
                row = None

            row_item.Remove(self.__table)

            del self.__items[itemid]
            self.__items_order.remove(itemid)

            self.__ReorderItemsInTable(row)

            rows = len(self.__items_order)
            self.__table.resize(rows, 2)

        def AppendItem(self, row_item):
            self.InsertItem(self.GetItemCount(), row_item)

        def InsertItem(self, row, row_item):
            rows = len(self.__items_order)
            self.__table.resize(rows + 1, 2)

            self.__items[row_item.GetItemId()] = row_item

            self.__items[row_item.GetItemId()] = row_item
            self.__items_order.insert(row, row_item.GetItemId())
            self.__ReorderItemsInTable(row)

        def __ReorderItemsInTable(self, row):
            for i, itemid in enumerate(self.__items_order[row:], row):
                row_item = self.__items[itemid]
                row_item.Move(i, self.__table)

    class COtherItemManager(object):
        def __init__(self, vbox, vpaned):
            self.__vbox = vbox
            self.__vpaned = vpaned
            self.__fixed_items_count = len(self.__vpaned.get_children())
            self.__items = {}

        def __HasVBoxOtherItems(self):
            return len(self.__vbox.get_children()) > self.__fixed_items_count

        def AddItem(self, item):
            widget = item.GetItem().GetWidget()

            self.__items[item.GetItemId()] = item

            vpaned_count = len(self.__vpaned.get_children())
            if vpaned_count == 0:
                self.__vpaned.add1(widget)
            elif vpaned_count == 1:
                self.__vpaned.add2(widget)
            else:
                self.__vbox.pack_start(widget)

        def RemoveItem(self, item):
            widget = item.GetItem().GetWidget()

            del self.__items[item.GetItemId()]

            if self.__vpaned.get_child1() == widget:
                self.__vpaned.remove(widget)
                child2 = self.__vpaned.get_child2()
                if child2 is not None:
                    self.__vpaned.remove(child2)
                    self.__vpaned.add1(child2)
                    self.__MoveFirstOtherItemToVPaned()
            elif self.__vpaned.get_child2() == widget:
                self.__vpaned.remove(widget)
                self.__MoveFirstOtherItemToVPaned()
            else:
                self.__vbox.remove(widget)

        def __MoveFirstOtherItemToVPaned(self):
            if not self.__HasVBoxOtherItems():
                return
            if self.__vpaned.get_child2() is not None:
                raise StandardError("VPaned contains second child, cannot move first child from VBox there.")

            first = self.__vbox.get_children()[2]
            self.__vbox.remove(first)
            self.__vpaned.add2(first)

    class CDialogTabItem(object):
        def __init__(self, itemid, item, itemname):
            self.itemid = itemid
            self.item = item

        def GetItemId(self):
            return self.itemid

        def GetItem(self):
            return self.item

    class COtherItem(CDialogTabItem):
        def __init__(self, itemid, item, itemname):
            CDialogTab.CDialogTabItem.__init__(self, itemid, item, itemname)
            if isinstance(item, CTextArea):
                item.GetWidget().set_label(itemname)

    class CTableRowItem(CDialogTabItem):
        def __init__(self, itemid, item, itemname):
            CDialogTab.CDialogTabItem.__init__(self, itemid, item, itemname)
            lbl = gtk.Label(itemname)
            lbl.show()
            self.__align = gtk.Alignment(0, 0.5)
            self.__align.set_padding(0, 0, 5, 0)
            self.__align.show()
            self.__align.add(lbl)

        def GetItemId(self):
            return self.itemid

        def Move(self, row, table):
            self.Remove(table)
            table.attach(self.__align, 0, 1, row, row + 1, )
            table.attach((self.item.GetWidget()), 1, 2, row, row + 1)

        def Remove(self, table):
            table.remove(self.__align)
            table.remove(self.item.GetWidget())