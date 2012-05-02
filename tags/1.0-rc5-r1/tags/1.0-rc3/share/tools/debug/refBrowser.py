import gc
import sys

class Browser(object):
    def __init__(self, obj, collectFirst = True):
        self.__obj = [obj]
        self.__collectFirst = collectFirst
    
    def up(self):
        if len(self.__obj) > 1:
            del self.__obj[-1]
        
        self.list()
    
    def go(self, id):
        all = self.__get()
        self.__obj.append(all[id])
        del all
        
        self.list()
    
    def list(self):
        all = self.__get()
        for id, obj in enumerate(all):
            print "%s:" % id
            print '    ', obj
    
    def current(self):
        return self.__obj[-1]
    
    def __get(self):
        if self.__collectFirst:
            gc.collect()
        
        ret = gc.get_referrers(self.current())
        
        frames = self.__listFrames()
        ret = [r for r in ret if r not in frames]
        
        ret.remove(self.__obj)
        
        return ret
    
    def __listFrames(self):
        frames = list()
        f = sys._getframe()
        frames.append(f)
        while f:
            f = f.f_back
            frames.append(f)
        
        return frames
