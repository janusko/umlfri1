#!/usr/bin/python
import sys
import os

port = int(os.environ['UMLFRI_PORT'])
path = os.environ['UMLFRI_PATH']
rootPath = os.environ['UMLFRI_ROOT']
uri = os.environ['UMLFRI_URI']

sys.path.insert(0, rootPath)
sys.path.insert(0, path)

import plugin
from lib.Addons.Plugin.Client.Interface import CInterface

interface = CInterface(port)
interface._Init(uri)
plugin.pluginMain(interface)
interface.Mainloop()
