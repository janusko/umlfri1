#!/usr/bin/python
import sys

import os

uri = os.environ['UMLFRI_URI']

if False:
    import re
    import os.path
    class Trace(object):
        def __init__(self):
            LOG_NAME = re.sub("[^a-zA-Z0-9]", "_", uri)
            if os.name == 'nt':
                LOG_PATH="c:\\temp"
            else:
                LOG_PATH="/tmp"
            self.LOG=file(os.path.join(LOG_PATH, LOG_NAME), 'w')
        
        def trace(self, frame, event, arg):
            self.LOG.write("%s:%d\t%s\t%s"%(frame.f_code.co_filename, frame.f_lineno, event, arg))
            self.LOG.write("\n")
            self.LOG.flush()
            
            return self.trace
    
    sys.settrace(Trace().trace)

pin = int(os.environ['UMLFRI_PIN'])
pout = int(os.environ['UMLFRI_POUT'])

if os.name == 'nt':
    import msvcrt
    pin = msvcrt.open_osfhandle(pin, os.O_RDONLY)
    pout = msvcrt.open_osfhandle(pout, os.O_APPEND)

if 'UMLFRI_ROOT' in os.environ:
    rootPath = os.environ['UMLFRI_ROOT']
    sys.path.insert(0, rootPath)

path = os.environ['UMLFRI_PATH']
sys.path.insert(0, path)

import plugin
from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Addons.Plugin.Communication.Medium import CPipeMedium

pipe = CPipeMedium(pin, pout)
interface = CInterface(pipe)
interface._Init(uri)
plugin.pluginMain(interface)
interface.Mainloop()
