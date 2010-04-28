import gtk
import pygtk
from lib.Gui.frmPropertiesWidgets.GTK.Button import CButton
from lib.Gui.frmPropertiesWidgets.GTK.Dialog import CDialog
from lib.Gui.frmPropertiesWidgets.GTK.CheckButton import CCheckButton
from lib.Gui.frmPropertiesWidgets.Abstract.AbstractResponseDialog import CAbstractResponseDialog

class CResponseDialog(CAbstractResponseDialog):
    
    def __init__(self,title,parent):
        self.dialog=gtk.Dialog(title,parent.GetWidget(),gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT | gtk.WINDOW_TOPLEVEL)
        self.dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.response=None
        self.default_response=None
    
    def GetWidget(self):
        return self.dialog
    
    def Show(self):
        if self.default_response!=None:
            self.default_response.grab_focus()
        self.dialog.set_resizable(False)
        self.dialog.run()
    
    def Close(self):
        self.dialog.destroy()
        return self.response
    
    def SetQuestion(self,question):
        hbox=gtk.HBox()
        hbox.show()
        img=gtk.Image()
        img.set_from_stock(gtk.STOCK_DIALOG_QUESTION,gtk.ICON_SIZE_DIALOG)
        img.show()
        hbox.pack_start(img,False,False,10)
        lbl=gtk.Label(question)
        lbl.show()
        hbox.pack_start(lbl,False,False,5)
        self.dialog.vbox.pack_start(hbox,False,False)
    
    def SetWarning(self,warning):
        hbox=gtk.HBox()
        hbox.show()
        img=gtk.Image()
        img.set_from_stock(gtk.STOCK_DIALOG_WARNING,gtk.ICON_SIZE_DIALOG)
        img.show()
        hbox.pack_start(img,False,False,10)
        lbl=gtk.Label(warning)
        lbl.show()
        hbox.pack_start(lbl,False,False,5)
        self.dialog.vbox.pack_start(hbox,False,False)
    
    def SetToggleButton(self,button):
        algn=gtk.Alignment(0,0)
        algn.set_padding(20,5,10,0)
        algn.show()
        algn.add(button.GetWidget())
        self.dialog.vbox.pack_start(algn,False,False,)
    
    def AppendResponse(self,response,name,default=False):
        button=CButton(name)
        button.SetHandler('clicked',self.__SetResponse,tuple([response]))
        self.dialog.action_area.pack_start(button.GetWidget(),False,False)
        if default==True:
            self.default_response=button.GetWidget()
    
    def __SetResponse(self,data):
        self.response=data
        self.dialog.response(gtk.RESPONSE_NONE)