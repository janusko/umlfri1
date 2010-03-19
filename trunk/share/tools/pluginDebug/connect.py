import os.path
import sys

sys.path.append(os.path.abspath(os.path.join('..', '..', '..')))

from lib.Addons.Plugin.Client.Interface import CInterface

a = CInterface(int(sys.argv[1]))
