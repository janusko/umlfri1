import os.path
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..', '..')))

from lib.Addons.Plugin.Client.Interface import CInterface

a = CInterface(int(sys.argv[1]))
