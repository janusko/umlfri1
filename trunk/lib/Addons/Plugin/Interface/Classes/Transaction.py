from base import IBase

from lib.Addons.Plugin.Interface.Transaction import CTransaction

class ITransaction(IBase):
    __cls__ = CTransaction
    
    def GetAutocommit(him):
        return him.GetState() == 'autocommit'
    
    def SetAutocommit(him, value):
        if value:
            him.StartAutocommit()
        else:
            him.EndAutocommit()
    
    def Begin(him):
        him.BeginTransaction()
    
    def Commit(him):
        him.CommitTransaction()
    
    def Rollback(him):
        him.RollbackTransaction()
