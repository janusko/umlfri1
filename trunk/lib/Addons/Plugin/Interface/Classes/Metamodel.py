from base import IBase
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.decorators import *
from lib.Addons.Metamodel.Metamodel import CMetamodel
from lib.Exceptions import *

class IMetamodel(IBase):
    __cls__ = CMetamodel
    
    def GetUri(him):
        return him.GetUri()
    
    def GetVersion(him):
        return him.GetVersionString()
    
    def GetDiagram(him, name):
        return him.GetDiagramFactory().GetDiagram(name)
        
    def GetDiagrams(him):
        return list(him.GetDiagramFactory())
    
    def GetElements(him):
        return list(him.GetElementFactory().IterTypes())
    
    def GetConnection(him, name):
        return him.GetConnectionFactory().GetConnection(name)
    
    def GetConnections(him):
        return list(him.GetConnectionFactory().IterTypes())
    
    def GetDomains(him):
        return list(him.GetDomainFactory().IterTypes())
    
    def ListDir(him, path):
        try:
            return him.GetStorage().listdir(path)
        except:
            raise ParamValueError('invalid path')
    
    def ReadFile(him, path):
        try:
            return him.GetStorage().read_file(path)
        except:
            raise ParamValueError('invalid path')
        
