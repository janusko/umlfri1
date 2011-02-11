import os.path
import sys
import thread

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..', '..')))

from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Addons.Plugin.Communication.Medium import CSocketMedium

a = CInterface(CSocketMedium(int(sys.argv[1])))
thread.start_new(a.Mainloop, ())