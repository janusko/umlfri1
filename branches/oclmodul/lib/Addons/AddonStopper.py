class CAddonStopper(object):
    def __init__(self, manager, addons):
        self.__manager = manager
        self.__addons = addons
        self.__toStop = list(addons)
        self.__toWait = set()
        self.__cantStop = set()
        self.__revDeps = self.__CalculateRevDeps(manager.ListAddons())
    
    def Remaining(self):
        return len(self.__toStop)
    
    def GetDependencyTree(self):
        for addon in self.__toStop:
            yield self.__CreateDepTree(addon)

    def __CreateDepTree(self, addon):
        for dep in self.__revDeps[addon.GetDefaultUri()]:
            depAddon = self.__manager.GetAddon(dep.GetUri())
            
            if depAddon.IsRunning():
                yield 'running', self.__CalculateRevDeps(depAddon)
            else:
                yield 'stopped', self.__CalculateRevDeps(depAddon)
    
    def Step(self):
        for addon in self.__toStop[:]:
            self.__StopAddon(addon)
    
    def __StopAddon(self, addon):
        if addon.GetDefaultUri() in self.__toWait:
            if not addon.IsRunning():
                self.__toWait.remove(addon.GetDefaultUri())
                if addon in self.__toStop:
                    self.__toStop.remove(addon)
                return 'ok'
            else:
                return 'later'
        
        if not addon.IsRunning():
            return 'ok'
        
        if addon.GetDefaultUri() in self.__cantStop:
            return 'no'
        
        if not addon.CheckUmlFriDependencies():
            return 'no'
        
        can = 'ok'
        
        for dep in self.__revDeps.get(addon.GetDefaultUri(), ()):
            depAddon = self.__manager.GetAddon(dep)
            if depAddon.IsRunning():
                ret = self.__StopAddon(depAddon)
                if ret == 'no' or can == 'no':
                    can = 'no'
                elif can == 'later':
                    can = 'later'
                else:
                    can = ret
        
        if can == 'ok':
            addon.Disable()
            addon.Stop()
            if addon.IsRunning():
                if addon.GetRunInProcess():
                    self.__toWait.add(addon.GetDefaultUri())
            else:
                if addon in self.__toStop:
                    self.__toStop.remove(addon)
                can = 'later'
        return can

    def __CalculateRevDeps(self, addons):
        ret = {}
        for addon in addons:
            for dep in addon.GetDependencies():
                if dep.GetRequired():
                    ret.setdefault(dep.GetUri(), []).append(addon.GetDefaultUri())
        return ret
