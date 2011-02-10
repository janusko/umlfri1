#!/usr/bin/python
import sys
import os

port = eval(os.environ['UMLFRI_PORT'], {}, {})
uri = os.environ['UMLFRI_URI']

if 'UMLFRI_ROOT' in os.environ:
    rootPath = os.environ['UMLFRI_ROOT']
    sys.path.insert(0, rootPath)

path = os.environ['UMLFRI_PATH']
sys.path.insert(0, path)

import plugin
from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Addons.Plugin.Communication.Medium import SocketMedium, PipeMedium

sock = SocketMedium(port)
interface = CInterface(sock)
interface._Init(uri)
plugin.pluginMain(interface)
interface.Mainloop()
