#!/usr/bin/python

import lib.Warnings.List
lib.Warnings.List.WarningList.handle()

import lib.Depend
lib.Depend.check()

from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject

from lib.Clipboard import CClipboard
from lib.Gui.common import CApplication, argument

import os.path
import traceback

from lib.Project import CProject
from lib.Project import CRecentFiles
from lib.Project.Templates import CTemplateManager
from lib.Addons import CAddonManager

import lib.Gui
from lib.Gui import CBus
from lib.Gui.dialogs import CExceptionDialog, CErrorDialog

from lib.config import config
from lib.Distconfig import LOCALES_PATH, GUI_PATH
from lib.consts import SPLASH_TIMEOUT

from lib.Exceptions import UserException

__version__ = '1.0-rc1'

class Application(CApplication):
    windows = lib.Gui
    main_window = 'frmMain'
    textdomain = 'uml_fri'
    localespath = LOCALES_PATH
    
    guipath = GUI_PATH

    project = None
    canopen = True
    
    def __init__(self):
        self.warnings = lib.Warnings.List.WarningList()
        self.recentFiles = CRecentFiles()
        self.clipboard = CClipboard()
        self.bus = CBus()
        self.addonManager = CAddonManager()
        self.templateManager = CTemplateManager(self.addonManager)
        
        CApplication.__init__(self)
        
        gobject.timeout_add(SPLASH_TIMEOUT, self.GetWindow('frmSplash').Hide)
    
    def GetBus(self):
        return self.bus
    
    @argument("-o", "--open", True)
    def DoOpen(self, value):
        "Opens selected project file"
        if self.canopen:
            self.GetWindow('frmMain').LoadProject(value, False)
            self.canopen = False
            
    
    @argument("-n", "--new", True)
    def DoNew(self, value):
        "Creates new project from template"
        if self.canopen:
            self.GetWindow('frmMain').LoadProject(value, True)
            self.canopen = False
    
    @argument(None, "--install-addon", True)
    def DoInstallAddon(self, value):
        "Install addon for UML .FRI"
        if self.canopen:
            self.canopen = False
            addon = self.addonManager.LoadAddon(value)
            
            self.GetWindow('frmSplash').Hide()
            
            if addon is None:
                CErrorDialog(None, _("Addon could not be installed")).run()
                return
            
            if self.GetWindow("frmInstallAddon").ShowDialog(self.GetWindow("frmMain"), addon):
                self.addonManager.InstallAddon(addon)
                return
    
    @argument()
    def DoArguments(self, *files):
        "File to open"
        if self.canopen:
            self.GetWindow('frmMain').LoadProject(files[0], False)
            self.canopen = False
    
    def GetRecentFiles(self):
        return self.recentFiles
    
    def ProjectInit(self):
        if self.project is None:
            self.project = CProject(self.addonManager)
            
    def ProjectDelete(self):
        self.project = None
        
    def GetProject(self):
        return self.project
    
    def GetTemplateManager(self):
        return self.templateManager
    
    def GetClipboard(self):
        return self.clipboard
    
    def cw_FileChooserWidget(self, str1, str2, int1, int2):
        if str1:
            action = getattr(gtk, 'FILE_CHOOSER_ACTION_%s'%str1.upper())
        else:
            action = gtk.FILE_CHOOSER_ACTION_OPEN
        widget = gtk.FileChooserWidget(action)
        widget.show()
        return widget
    
    def DisplayException(self, exccls, excobj, tb):
        if issubclass(exccls, UserException) and not __debug__:
            text = _('An exception has occured:')+ '\n\n<b>'+exccls.__name__ +':</b> '+ str(excobj)
            CExceptionDialog(None, text).run()
        else:
            if __debug__:
                traceback.print_exc()
            win = self.GetWindow('frmException')
            win.SetParent(self.GetWindow('frmMain'))
            win.SetErrorLog(exccls, excobj, tb)
            win.Show()
    
    def Quit(self):
        CApplication.Quit(self)
        config.Save()
        self.addonManager.Save()
        self.recentFiles.SaveRecentFiles()

if __name__ == '__main__':
    Application().Main()
