from lib.Depend.gtk2 import gtk, gobject

from lib.Drawing.Canvas.GtkPlus import PixmapFromPath

from common import event, CWindow
from dialogs import CQuestionDialog

import webbrowser

class CfrmInstallAddon(CWindow):
    name = 'frmInstallAddon'
    glade = 'addons.glade'
    
    widgets = (
        'cmdInstallAddonYes', 'lblInstallAddonCounter',
        'lblInstallAddonHomepageLabel', 'lblInstallAddonLicenseLabel', 'lblInstallAddonDescriptionLabel',
        
        'imgInstallAddonIcon',
        'lblInstallAddonName', 'lblInstallAddonVersion', 'lblInstallAddonType',
        'lblInstallAddonAuthor', 'lbInstallAddonHomepage', 'lblInstallAddonLicense',
        'lblInstallAddonDescription',
    )
    
    def counter(self):
        if self.__cnt <= 0:
            self.cmdInstallAddonYes.set_sensitive(True)
            self.lblInstallAddonCounter.set_label('')
            
            return False
        else:
            self.cmdInstallAddonYes.set_sensitive(False)
            self.lblInstallAddonCounter.set_label(' (%d)'%self.__cnt)
            self.__cnt -= 1
            
            return True

    def ShowDialog(self, parent, addon):
        self.__cnt = 5
        
        self.counter()
        gobject.timeout_add(1000, self.counter)
        
        icon = addon.GetIcon()
        if icon is None:
            self.imgInstallAddonIcon.clear()
        else:
            self.imgInstallAddonIcon.set_from_pixbuf(PixmapFromPath(addon.GetStorage(), icon))
        
        self.lblInstallAddonName.set_markup("<big><b>%s</b></big>"%addon.GetName())
        self.lblInstallAddonVersion.set_label(addon.GetVersion())
        if addon.GetType() == 'metamodel':
            self.lblInstallAddonType.set_label(_("metamodel"))
        else:
            return
        
        self.lblInstallAddonAuthor.set_label(', '.join(addon.GetAuthor()))
        
        license = addon.GetLicenseName()
        if license is None:
            self.lblInstallAddonLicense.hide()
            self.lblInstallAddonLicenseLabel.hide()
        else:
            self.lblInstallAddonLicense.show()
            self.lblInstallAddonLicenseLabel.show()
            self.lblInstallAddonLicense.set_label(license)
        
        homepage = addon.GetHomepage()
        if homepage is None:
            self.lbInstallAddonHomepage.hide()
            self.lblInstallAddonHomepageLabel.hide()
        else:
            self.lbInstallAddonHomepage.show()
            self.lblInstallAddonHomepageLabel.show()
            self.lbInstallAddonHomepage.set_uri(homepage)
            self.lbInstallAddonHomepage.set_label(homepage)
        
        desc = addon.GetDescription()
        if desc is None:
            self.lblInstallAddonDescription.hide()
            self.lblInstallAddonDescriptionLabel.hide()
        else:
            self.lblInstallAddonDescription.show()
            self.lblInstallAddonDescriptionLabel.show()
            self.lblInstallAddonDescription.set_label(desc)
        
        self.form.set_transient_for(parent.form)
        
        try:
            return self.form.run() == gtk.RESPONSE_YES
        finally:
            self.Hide()
    
    @event("lbInstallAddonHomepage", "clicked")
    def on_lbInstallAddonHomepage_clicked(self, widget):
        webbrowser.open_new_tab(widget.get_uri())
