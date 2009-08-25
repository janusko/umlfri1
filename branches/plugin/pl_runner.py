#!/usr/bin/python
import sys
from lib.Addons.Plugin.Client.Interface import CInterface

port = int(sys.argv[1])
interface = CInterface(port)

path = sys.argv[2]

if len(sys.argv) > 3:
    uri = sys.argv[3]
    password = sys.argv[4]

    interface._Init(uri, password)

sys.path.insert(0, path)

import plugin
plugin.pluginMain(interface)
interface.WaitTillClosed()
