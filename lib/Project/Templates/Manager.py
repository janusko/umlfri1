from lib.consts import PROJECT_TPL_EXTENSION
from lib.Distconfig import TEMPLATES_PATH, USERDIR_PATH
from lib.Storages import open_storage
from lib.Base import CBaseObject

from Template import CTemplate

import os
import os.path

class CTemplateManager(CBaseObject):
    def __init__(self, addonManager):
        self.__dirs = (TEMPLATES_PATH, os.path.join(USERDIR_PATH, 'templates'))
        self.__addonManager = addonManager
    
    def GetAllTemplates(self):
        for dirname in self.__dirs:
            if os.path.exists(dirname):
                for filename in os.listdir(dirname):
                    if not filename.endswith(PROJECT_TPL_EXTENSION):
                        continue
                    
                    storage = open_storage(os.path.join(dirname, filename))
                    
                    if storage is None:
                        continue
                    
                    if storage.exists('icon.png'):
                        icon = 'icon.png'
                    else:
                        icon = None
                    
                    yield CTemplate(filename.rsplit('.', 1)[0], storage, 'content.xml', icon)
        
        for type in ('metamodel', 'composite'):
            for addon in self.__addonManager.ListEnabledAddons(type):
                for name, icon, path in addon.GetComponent().GetTemplates():
                    if name is None:
                        name = path.replace('\\', '/').rsplit('/', 1)[-1].rsplit('.', 1)[0]
                    
                    if icon is None:
                        icon = addon.GetIcon()
                    
                    yield CTemplate(name, addon.GetStorage(), path, icon)
