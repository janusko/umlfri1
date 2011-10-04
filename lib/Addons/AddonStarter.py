class CAddonStarter(object):
    def __init__(self, manager, addons):
        self.__manager = manager
        self.__toStart = list(addons)
        self.__toWait = set()
        self.__cantStart = {}
    
    def ToStartCount(self):
        return len(self.__toStart)
    
    def GetDependencyTree(self):
        for addon in self.__toStart:
            yield self.__CreateDepTree(addon)

    def __CreateDepTree(self, addon):
        for dep in addon.GetDependencies():
            depAddon = self.__manager.GetAddon(dep.GetUri())
            
            if depAddon.GetRequired():
                if depAddon is None:
                    return 'missing', dep.GetUri(), ()
                elif depAddon.IsRunning():
                    return 'running', depAddon, self.__CreateDepTree(depAddon)
                else:
                    return 'stopped', depAddon, self.__CreateDepTree(depAddon)
            else:
                if depAddon is not None and depAddon.IsRunning():
                    return 'running', depAddon, self.__CreateDepTree(depAddon)
    
    def Step(self):
        for addon in self.__toStart[:]:
            self.__StartAddon(addon)
    
    def __StartAddon(self, addon):
        if addon.GetDefaultUri() in self.__toWait:
            if addon.IsRunning():
                self.__toWait.remove(addon.GetDefaultUri())
                self.__toStart.remove(addon)
                return 'ok'
            else:
                return 'later'
        
        if addon.IsRunning():
            return 'ok'
        
        if addon.GetDefaultUri() in self.__cantStart:
            return 'no'
        
        if not addon.CheckUmlFriDependencies():
            return 'no'
        
        can = 'ok'
        
        for dep in addon.GetDependencies():
            depAddon = self.__manager.GetAddon(dep.GetUri())
            if not depAddon.IsRunning():
                ret = self.__StartAddon(depAddon)
                if ret == 'no' or can == 'no':
                    can = 'no'
                elif can == 'later':
                    can = 'later'
                else:
                    can = ret
        
        if can == 'ok':
            addon.Enable()
            addon.Start()
            if addon.IsRunning():
                if addon in self.__toStart:
                    self.__toStart.remove(addon)
            else:
                if addon.GetRunInProcess():
                    self.__toWait.add(addon.GetDefaultUri())
                can = 'later'
        return can
