from .Decorators import params, mainthread, polymorphic

from . import Project
from . import Diagram
from . import GuiManager
from . import Transaction
from . import Template
from . import FileTypeManager

class IAdapter(object):
    def __init__(self, plugin, adapter):
        self.__plugin = plugin
        self.__adapter = adapter
    
    @property
    def uid(self):
        return self.__adapter.GetUID()
    
    def GetProject(self):
        adapter = self.__adapter.GetProject()
        if adapter is None:
            return None
        return Project.IProject(self.__plugin, adapter)
    
    def GetCurrentDiagram(self):
        diagram = self.__adapter.GetCurrentDiagram()
        if diagram is None:
            return None
        return Diagram.IDiagram(self.__plugin, diagram)
    
    @params(object)
    def SetCurrentDiagram(self, value):
        if value is not None:
            value = value._diagram
        self.__adapter.SelectDiagramTab(value)
    
    # TODO: new system for notifications (notification bus)
    
    def GetGuiManager(self):
        return GuiManager.IGuiManager(self.__plugin, self.__adapter.GetGuiManager())
    
    @params(str)
    def LoadProject(self, fileName):
        self.__adapter.LoadProject(fileName)
    
    def GetTransaction(self):
        return Transaction.ITransaction(self.__plugin.GetTransaction())
    
    def GetTemplates(self):
        for template in self.__adapter.GetTemplateManager().GetAllTemplates():
            yield Template.ITemplate(template)
    
    def GetFileTypeManager(self):
        return FileTypeManager.IFileTypeManager(self.__plugin, self.__adapter.GetFileTypeManager())
    
    def AttachProjectOpened(self):
        pass # TODO: add support for projectOpened event
    
    def DetachProjectOpened(self):
        pass
