from lib.config import config

import os
import os.path
import subprocess

class CPythonStarter(object):
    __pl_runner = os.path.join(os.path.dirname(__file__), 'pl_runner.py')
    
    def __init__(self, plugin):
        self.__plugin = plugin
    
    def Start(self):
        rootPath = config['/Paths/Root']
        
        port = self.__plugin.GetPluginManager().GetPort()
        path = self.__plugin.GetPath()
        uri = self.__plugin.GetUri()
        
        self.__process = subprocess.Popen([self.__pl_runner, str(port), rootPath, path, uri], shell = (os.name == 'nt'))
