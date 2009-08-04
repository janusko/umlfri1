class CTransaction(object):
    
    def __init__(self, interface):
        self.interface = interface
    
    def __enter__(self):
        self.interface.BeginTransaction()
    
    def __exit__(self, type, value, traceback):
        if type is None:
            self.interface.CommitTransaction()
        else:
            self.interface.RollbackTransaction()
    