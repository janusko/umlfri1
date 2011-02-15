import time, threading

class CWatchdog(object):
    
    def __init__(self, manager):
        self.__manager = manager
        self.__online = True
        threading.Thread(target = self.__mainloop).start()
        
    def __mainloop(self):
        while self.__online:
            time.sleep(0.5)
            for plugin in self.__manager.GetPluginList():
                if self.__online:
                    if not plugin.IsAlive():
                        plugin.Dispose()
    
    def Stop(self):
        self.__online = False
