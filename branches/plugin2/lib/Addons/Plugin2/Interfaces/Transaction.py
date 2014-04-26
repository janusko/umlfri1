from .Decorators import params, mainthread, polymorphic

class ITransaction(object):
    def __init__(self, transaction):
        self.__transaction = transaction
    
    @property
    def uid(self):
        return self.__transaction.GetUID()
    
    def GetAutocommit(self):
        return self.__transaction.GetState() == 'autocommit'
    
    @params(bool)
    def SetAutocommit(self, value):
        if value:
            self.__transaction.StartAutocommit()
        else:
            self.__transaction.EndAutocommit()
    
    def Begin(self):
        self.__transaction.BeginTransaction()
    
    def Commit(self):
        self.__transaction.CommitTransaction()
    
    def Rollback(self):
        self.__transaction.RollbackTransaction()
