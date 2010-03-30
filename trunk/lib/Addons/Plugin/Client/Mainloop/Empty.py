import thread

class CEmpty(object):
    
    def __init__(self):
        self.lock = thread.allocate()
        self.lock.acquire()
        self.stop = False
        self.buffer = []
        self.buflock = thread.allocate()
        
    def Mainloop(self):
        while True:
            self.lock.acquire()
            if self.stop:
                return
            with self.buflock:
                if self.buffer:
                    fun, args, kwds = self.buffer.pop(0)
                else:
                    fun = None
            if fun:
                fun(*args, **kwds)
            
            with self.buflock:
                if self.buffer and self.lock.locked():
                    self.lock.release()
            
    def Call(self, callable, *args, **kwds):
        with self.buflock:
            self.buffer.append((callable, args, kwds))
            if self.lock.locked():
                self.lock.release()
    
    def Stop(self):
        self.stop = True
        with self.buflock:
            if self.lock.locked():
                self.lock.release()
