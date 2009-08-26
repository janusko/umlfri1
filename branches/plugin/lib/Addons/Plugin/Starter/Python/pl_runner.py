#!/usr/bin/python
import sys

port = int(sys.argv[1])
path = sys.argv[2]
rootPath = sys.argv[3]
uri = sys.argv[4]

sys.path.insert(0, rootPath)
sys.path.insert(0, path)

import plugin
from lib.Addons.Plugin.Client.Interface import CInterface

interface = CInterface(port)
interface._Init(uri)
plugin.pluginMain(interface)
interface.WaitTillClosed()
