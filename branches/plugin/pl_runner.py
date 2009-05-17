#!/usr/bin/python
import sys
from lib.Plugin.Client.Interface import CInterface
from lib.config import config

port = int(sys.argv[1])
interface = CInterface(port)

name = sys.argv[2]
sys.path.append(config['/Paths/Plugins'])
plugin = __import__(name)
plugin.main(interface)
interface.WaitTillClosed()


