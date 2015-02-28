from .Decorators import params, mainthread, polymorphic

class ITemplate(object):
    def __init__(self, plugin, template):
        self.__plugin = plugin
        self.__template = template
    
    @property
    def uid(self):
        return self.__template.GetUID()
    
    def GetName(self):
        return self.__template.GetName()
    
    def GetMetamodelUri(self):
        return self.__template.GetMetamodelUri()
    
    def CreateNewProject(self):
        return self.__plugin.GetAdapter().CreateNewProject(self.__template)
