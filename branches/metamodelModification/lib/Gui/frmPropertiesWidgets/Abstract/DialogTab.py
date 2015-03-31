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

    def GetFrame(self):
        return self.frame

    def GetItemCount(self):
        return len(self.items)

    def AppendItem(self, itemid, item, itemname):
        if itemid in self.items:
            raise KeyError("Item with id {0} already exists".format(itemid))

        rows = self.GetItemCount()
        self.items[itemid] = item
        if isinstance(item, CComboBox) or isinstance(item, CEditableComboBox) or \
                isinstance(item, CEditBox) or isinstance(item, CEditBoxWithButton):
            self.__table.resize(rows + 1, 2)
            lbl = gtk.Label(itemname)
            lbl.show()
            align = gtk.Alignment(0, 0.5)
            align.set_padding(0, 0, 5, 0)
            align.show()
            align.add(lbl)
            self.__table.attach(align, 0, 1, rows, rows + 1, )
            self.__table.attach((item.GetWidget()), 1, 2, rows, rows + 1)
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
