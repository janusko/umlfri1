import gtk
from lib.Gui.frmPropertiesWidgets import CEditableComboBox, CEditBoxWithButton, CEditBox, CComboBox, CTextArea, CTable


class CDialogTab(object):
    def __init__(self):
        self.frame = gtk.Frame()
        self.items = {}
        self.table_items_order = []

        self.__vbox = gtk.VBox(False)
        self.frame.add(self.__vbox)

        self.__table = gtk.Table(0, 2)
        self.__table.set_col_spacings(5)
        self.__table.set_row_spacings(1)
        self.__vbox.pack_start(self.__table, False, False, 0)

        self.__vpaned = gtk.VPaned()
        self.__vbox.pack_start(self.__vpaned)

        self.frame.show_all()

    def GetFrame(self):
        return self.frame

    def GetItemCount(self):
        return len(self.items)

    def RemoveItem(self, itemid):
        if itemid not in self.items:
            raise KeyError("Item with id {0} already exists".format(itemid))

        item = self.items[itemid]

        if isinstance(item, CComboBox) or isinstance(item, CEditableComboBox) or \
                isinstance(item, CEditBox) or isinstance(item, CEditBoxWithButton):
            self.__RemoveTableRowItem(item)

    def AppendItem(self, itemid, item, itemname):
        if itemid in self.items:
            raise KeyError("Item with id {0} already exists".format(itemid))

        rows = self.GetItemCount()
        self.items[itemid] = item
        if isinstance(item, CComboBox) or isinstance(item, CEditableComboBox) or \
                isinstance(item, CEditBox) or isinstance(item, CEditBoxWithButton):
            row_item =  CDialogTab.CTableRowItem(itemid, item, itemname)
            self.__InsertTableRowItem(rows, row_item)
        elif isinstance(item, CTextArea):
            if len(self.__vpaned.get_children()) < 1:
                self.__vpaned.add1(item.GetWidget())
            elif len(self.__vpaned.get_children()) < 2:
                self.__vpaned.add2(item.GetWidget())
            else:
                self.__vbox.pack_start(item.GetWidget(), True, True)
            item.GetWidget().set_label(itemname)
        elif isinstance(item, CTable):
            if len(self.__vpaned.get_children()) < 1:
                self.__vpaned.add1(item.GetWidget())
            elif len(self.__vpaned.get_children()) < 2:
                self.__vpaned.add2(item.GetWidget())
            else:
                self.__vbox.pack_start(item.GetWidget(), True, True)

    def __RemoveTableRowItem(self, row_item):
        for i, itemid in enumerate(self.table_items_order):
            if itemid == row_item.GetItemId():
                row = i
                break
        else:
            row = None

        row_item.Remove(self.__table)

        del self.items[itemid]
        self.table_items_order.remove(itemid)

        self.__ReorderItemsInTable(row)

        rows = len(self.table_items_order)
        self.__table.resize(rows, 2)

    def __InsertTableRowItem(self, row, row_item):
        self.items[row_item.GetItemId()] = row_item
        self.table_items_order.insert(row, row_item.GetItemId())
        self.__ReorderItemsInTable(row)

    def __ReorderItemsInTable(self, row):
        for i, itemid in enumerate(self.table_items_order[row:], row):
            row_item = self.items[itemid]
            row_item.Move(i, self.__table)

    class CTableRowItem(object):
        def __init__(self, itemid, item, itemname):
            self.itemid = itemid
            self.item = item
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

        def Append(self, table):
            rows = len(table.get_children())
            table.resize(rows + 1, 2)
            self.Move(rows, table)

        def Remove(self, table):
            table.remove(self.__align)
            table.remove(self.item.GetWidget())