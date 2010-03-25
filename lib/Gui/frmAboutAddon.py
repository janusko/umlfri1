from lib.Depend.gtk2 import gtk, gobject

from lib.Drawing.Canvas.GtkPlus import PixmapFromPath

from common import event, CWindow
from dialogs import CQuestionDialog

import webbrowser

class CfrmAboutAddon(CWindow):
    name = 'frmAboutAddon'
    glade = 'addons.glade'
    
    widgets = (
        'lblAboutAddonHomepageLabel', 'lblAboutAddonLicenseLabel', 'lblAboutAddonDescriptionLabel',
        
        'imgAboutAddonIcon',
        'lblAboutAddonName', 'lblAboutAddonVersion', 'lblAboutAddonType',
        'lblAboutAddonAuthor', 'lbAboutAddonHomepage', 'lblAboutAddonLicense',
        'lblAboutAddonDescription', 'lblAboutAddonCopyright'
    )

    def ShowDialog(self, parent, addon):
        icon = addon.GetIcon()
        if icon is None:
            self.imgAboutAddonIcon.clear()
        else:
            self.imgAboutAddonIcon.set_from_pixbuf(PixmapFromPath(addon.GetStorage(), icon))
        
        self.lblAboutAddonName.set_markup("<big><b>%s</b></big>"%addon.GetName())
        self.lblAboutAddonVersion.set_label(addon.GetVersion())
        if addon.GetType() == 'metamodel':
            self.lblAboutAddonType.set_label(_("metamodel"))
        else:
            self.lblAboutAddonType.set_label(_("plugin"))
        
        self.lblAboutAddonAuthor.set_label(', '.join(addon.GetAuthor()))
        
        license = addon.GetLicenseName()
        if license is None:
            self.lblAboutAddonLicense.hide()
            self.lblAboutAddonLicenseLabel.hide()
        else:
            self.lblAboutAddonLicense.show()
            self.lblAboutAddonLicenseLabel.show()
            self.lblAboutAddonLicense.set_label(license)
        
        homepage = addon.GetHomepage()
        if homepage is None:
            self.lbAboutAddonHomepage.hide()
            self.lblAboutAddonHomepageLabel.hide()
        else:
            self.lbAboutAddonHomepage.show()
            self.lblAboutAddonHomepageLabel.show()
            self.lbAboutAddonHomepage.set_uri(homepage)
            self.lbAboutAddonHomepage.set_label(homepage)
        
        desc = addon.GetDescription()
        if desc is None:
            self.lblAboutAddonDescription.hide()
            self.lblAboutAddonDescriptionLabel.hide()
        else:
            self.lblAboutAddonDescription.show()
            self.lblAboutAddonDescriptionLabel.show()
            self.lblAboutAddonDescription.set_label(desc)
        
        self.lblAboutAddonCopyright.hide()
        
        self.form.set_transient_for(parent.form)
        
        self.form.run()
        self.Hide()
    
    @event("lbAboutAddonHomepage", "clicked")
    def on_lbAboutAddonHomepage_clicked(self, widget):
        webbrowser.open_new_tab(widget.get_uri())
