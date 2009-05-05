class CFuture(object):
    
    def __init__(self, lock, dict, key, dictlock):
        self.lock = lock
        self.hasresult = False
        self.result = None
        self.dict = dict
        self.key = key
        self.dictlock = dictlock
    
    def __call__(self):
        if not self.hasresult:
            self.lock.acquire()
            self.result = self.dict[self.key]
            self.hasresult = True
            self.dictlock.acquire()
            del self.dict[self.key]
            self.dictlock.release()
        return self.result
    
    def IsReady(self):
        return self.hasresult or not self.lock.locked()
