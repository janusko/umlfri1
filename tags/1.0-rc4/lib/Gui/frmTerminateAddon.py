from lib.Depend.gtk2 import gtk, pango, glib

import os.path
import webbrowser

import lib.consts
from lib.Drawing.Canvas.GtkPlus import PixmapFromPath

from common import event, CWindow
from dialogs import CQuestionDialog
import time

class CfrmTerminateAddon(CWindow):
    name = 'frmTerminateAddon'
    glade = 'addons.glade'
    
    widgets = (
        'lblTerminateAddonHomepageLabel',
        
        'imgTerminateAddonIcon',
        'lblTerminateAddonName', 'lblTerminateAddonVersion', 'lblTerminateAddonType',
        'lblTerminateAddonAuthor', 'lbTerminateAddonHomepage',
    )

    def ShowDialog(self, parent, addon):
        icon = addon.GetIcon()
        if icon is None:
            self.imgTerminateAddonIcon.clear()
        else:
            try:
                self.imgTerminateAddonIcon.set_from_pixbuf(PixmapFromPath(addon.GetStorage(), icon))
            except:
                self.imgTerminateAddonIcon.clear()
        
        self.lblTerminateAddonName.set_markup("<big><b>%s</b></big>"%addon.GetName())
        self.lblTerminateAddonVersion.set_label(addon.GetVersion())
        if addon.GetType() == 'metamodel':
            self.lblTerminateAddonType.set_label(_("metamodel"))
        elif addon.GetType() == 'plugin':
            self.lblTerminateAddonType.set_label(_("plugin"))
        elif addon.GetType() == 'composite':
            self.lblTerminateAddonType.set_label(_("metamodel+plugin"))
        else:
            return
        
        self.lblTerminateAddonAuthor.set_label(', '.join(addon.GetAuthor()))
        
        homepage = addon.GetHomepage()
        if homepage is None:
            self.lbTerminateAddonHomepage.hide()
            self.lblTerminateAddonHomepageLabel.hide()
        else:
            self.lbTerminateAddonHomepage.show()
            self.lblTerminateAddonHomepageLabel.show()
            self.lbTerminateAddonHomepage.set_uri(homepage)
            self.lbTerminateAddonHomepage.set_label(homepage)
        
        self.form.set_transient_for(parent.form)
        
        resp = self.form.run()
        self.Hide()
        
        return resp == gtk.RESPONSE_OK
    
