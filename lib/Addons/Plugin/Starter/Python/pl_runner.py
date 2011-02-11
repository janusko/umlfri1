#!/usr/bin/python
import sys
import os

pin = int(os.environ['UMLFRI_PIN'])
pout = int(os.environ['UMLFRI_POUT'])

if os.name == 'nt':
    import msvcrt
    pin = msvcrt.open_osfhandle(pin, os.O_RDONLY)
    pout = msvcrt.open_osfhandle(pout, os.O_APPEND)

uri = os.environ['UMLFRI_URI']

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
