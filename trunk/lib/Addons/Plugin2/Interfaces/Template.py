from ..PluginBase import params, mainthread, polymorphic

class ITemplate(object):
    def __init__(self, plugin, template):
        self.__plugin = plugin
        self.__template = template
    
    def GetName(self):
        return self.__template.GetName()
    
    def GetMetamodelUri(self):
        return self.__template.GetMetamodelUri()
    
    def CreateNewProject(self):
        return self.__plugin.GetAdapter().CreateNewProject(self.__template)
