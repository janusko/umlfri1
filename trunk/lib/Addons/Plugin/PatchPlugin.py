import sys
import types
import re
import os.path

class CPatchPlugin(object):
    __reModuleName = re.compile('[^a-zA-Z0-9]')
    
    def __init__(self, params, addonNamespace, addonPath, patchModule):
        self.__addonNamespace = addonNamespace
        
        self.__addonPath = addonPath
        self.__patchModule = patchModule
        
        self.__params = params
        
        self.__obj = None
    
    def __MakeObject(self):
        if 'plugins' not in sys.modules:
            sys.modules['plugins'] = types.ModuleType('plugins')
        
        addonModule = self.__reModuleName.sub('_', self.__addonNamespace)
        
        addonModuleFQN = 'plugins.%s'%addonModule
        patchModuleFQN = 'plugins.%s.%s'%(addonModule, self.__patchModule)
        
        if addonModuleFQN not in sys.modules:
            module = sys.modules[addonModuleFQN] = types.ModuleType(addonModule)
            module.__path__ = [self.__addonPath]
            
            setattr(sys.modules['plugins'], addonModule, module)
        
        module = __import__(patchModuleFQN)
        module = getattr(module, addonModule)
        module = getattr(module, self.__patchModule)
        
        self.__obj = module.Plugin(*self.__params)
    
    def Start(self):
        if self.__obj is None:
            self.__MakeObject()
        
        self.__obj.Start()
    
    def Stop(self):
        self.__obj.Stop()
