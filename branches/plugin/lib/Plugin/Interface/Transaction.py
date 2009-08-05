from lib.Exceptions import *
#~ import lib.debug

class CTransaction(object):
    #~ state = lib.debug.DebugAttribute('state')
    
    def __init__(self):
        self.buf = []
        self.state = 'unspecified'
    
    def Action(self, callable, args):
        if self.state == 'autocommit':
            callable(*args)
        elif self.state == 'transaction':
            self.buf.append((callable, args))
        else:
            raise TransactionModeUnspecifiedError()
    
    def StartAutocommit(self):
        if self.state == 'transaction':
            raise TransactionPendingError()
        else:
            self.state = 'autocommit'
    
    def BeginTransaction(self):
        if self.state in ('autocommit', 'unspecified'):
            self.state = 'transaction'
        else:
            raise TransactionPendingError()
    
    def CommitTransaction(self):
        if self.state == 'transaction':
            for callable, args in self.buf:
                callable(*args)
            self.state = 'unspecified'
        else:
            raise OutOfTransactionError()
    
    def RollbackTransaction(self):
        if self.state == 'transaction':
            self.buf = []
            self.state = 'unspecified'
        else:
            raise OutOfTransactionError()
            
