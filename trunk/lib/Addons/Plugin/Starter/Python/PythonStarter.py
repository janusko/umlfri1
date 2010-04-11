from lib.config import config
from lib.Distconfig import ROOT_PATH, IS_FROZEN

import os
import os.path
import subprocess

class CPythonStarter(object):
    if IS_FROZEN:
        __pl_runner = os.path.join(ROOT_PATH, 'bin', 'pl_runner.exe')
        __lib_root = None
    else:
        __pl_runner = os.path.join(os.path.dirname(__file__), 'pl_runner.py')
        __lib_root = ROOT_PATH
    
    def __init__(self, plugin):
        self.__plugin = plugin
    
    def Start(self):
        port = self.__plugin.GetPluginManager().GetPort()
        path = self.__plugin.GetPath()
        uri = self.__plugin.GetUri()
        
        env = os.environ.copy()
        env['UMLFRI_PORT'] = str(port)
        if self.__lib_root is not None:
            env['UMLFRI_ROOT'] = str(self.__lib_root)
        env['UMLFRI_PATH'] = str(path)
        env['UMLFRI_URI'] = str(uri)
        
        self.__process = subprocess.Popen([self.__pl_runner], shell = (os.name == 'nt'), env = env)
