import thread, time

class CWatchdog(object):
    
    def __init__(self, manager):
        self.__manager = manager
        self.__online = True
        thread.start_new_thread(self.__mainloop, ())
        
    def __mainloop(self):
        while self.__online:
            time.sleep(0.5)
            for plugin in self.__manager.GetPluginList():
                if self.__online:
                    if not plugin.IsAlive():
                        plugin.Dispose()
    
    def Stop(self):
        self.__online = False
