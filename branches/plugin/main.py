#!/usr/bin/python

import warnings
warnings.simplefilter('ignore', Warning)

import lib.Depend
lib.Depend.check()

from lib.Depend.gtk2 import gtk
from lib.Depend.gtk2 import gobject

from lib.Clipboard import CClipboard
from lib.Gui.common import CApplication, argument, CUserGui
import os.path

from lib.Project import CProject
from lib.Project import CRecentFiles

from lib.Gui import CfrmSplash, CfrmMain, CfrmAbout, CfrmProperties, CfrmOpen, CfrmSave, CfrmOptions, CfrmException, CPluginAdapter, CBus
from lib.Gui.dialogs import CExceptionDialog

from lib.config import config
from lib.consts import SPLASH_TIMEOUT

from lib.Exceptions import UserException
from lib.Plugin.Manager import CPluginManager
from lib.Plugin import Reference

__version__ = '1.0-beta20090309'

class Application(CApplication):
    windows = (CfrmSplash, CfrmMain, CfrmAbout, CfrmProperties, CfrmOpen, CfrmSave, CfrmOptions, CfrmException)
    glade = os.path.join(config['/Paths/Gui'], 'gui.glade')
    main_window = 'frmMain'
    textdomain = 'uml_fri'
    localespath = config['/Paths/Locales']

    project = None
    canopen = True
    
    def __init__(self):
        self.recentFiles = CRecentFiles()
        self.clipboard = CClipboard()
        self.bus = CBus()
        
        CApplication.__init__(self)
        self.UserGui= CUserGui(self)
        self.pluginManager = CPluginManager(self)
        self.pluginAdapter = CPluginAdapter(self)
        
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
            self.project = CProject(self)
            Reference.SetProject(self.project)
            
    def ProjectDelete(self):
        self.project = None
        
    def GetProject(self):
        return self.project
    
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
        if issubclass(exccls, UserException) and not lib.consts.DEBUG:
            text = _('An exception has occured:')+ '\n\n<b>'+exccls.__name__ +':</b> '+ str(excobj)
            CExceptionDialog(None, text).run()
        elif lib.consts.ERROR_TO_CONSOLE == True:
            raise # reraise the exception
        else: 
            win = self.GetWindow('frmException')
            win.SetParent(self.GetWindow('frmMain'))
            win.SetErrorLog(exccls, excobj, tb)
            win.Show()
    
    def Quit(self):
        self.UserGui.SaveConfig()
        CApplication.Quit(self)
        config.Save()
        self.recentFiles.SaveRecentFiles()
    
    def GetPluginManager(self):
        return self.pluginManager

if __name__ == '__main__':
    Application().Main()
