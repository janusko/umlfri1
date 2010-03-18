from lib.config import config
from lib.Distconfig import ROOT_PATH

import os
import os.path
import subprocess

class CPythonStarter(object):
    __pl_runner = os.path.join(os.path.dirname(__file__), 'pl_runner.py')
    
    def __init__(self, plugin):
        self.__plugin = plugin
    
    def Start(self):
        port = self.__plugin.GetPluginManager().GetPort()
        path = self.__plugin.GetPath()
        uri = self.__plugin.GetUri()
        
        env = os.environ.copy()
        env['UMLFRI_PORT'] = str(port)
        env['UMLFRI_ROOT'] = str(ROOT_PATH)
        env['UMLFRI_PATH'] = str(path)
        env['UMLFRI_URI'] = str(uri)
        
        self.__process = subprocess.Popen(self.__pl_runner, shell = (os.name == 'nt'), env = env)
