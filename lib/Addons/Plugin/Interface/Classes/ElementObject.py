from ast import literal_eval
from DomainObject import IDomainObject
from lib.Addons.Metamodel.Modifications.ModificationBundleFactory import CModificationBundleFactory
from lib.Addons.Plugin.Communication.ComSpec import *
from lib.Addons.Plugin.Interface.Classes.base import IBase
from lib.Addons.Plugin.Interface.decorators import *
from lib.Commands.Diagrams import CShowElementCommand
from lib.Commands.Project import CCreateConnectionObjectCommand, CCreateDiagramCommand, CCreateElementObjectCommand
from lib.Commands.Project.ApplyModificationBundles import CApplyModificationBundlesCommand
from lib.Commands.Project.RemoveModificationBundles import CRemoveModificationBundlesCommand
from lib.Drawing.Diagram import CDiagram
from lib.Drawing.Element import CElement
from lib.Elements.Object import CElementObject
from lib.Connections.Object import CConnectionObject
from lib.Domains.Object import CDomainObject
from lib.Exceptions import *
from lib.Project import CProjectNode

class IElementObject(IDomainObject):
    __cls__ = CElementObject

    def GetUid(him):
        return him.GetUID()

    def GetName(him):
        return him.GetName()
    
    def GetDiagrams(him):
        node = him.GetNode()
        if node is not None:
            return node.GetDiagrams()
    
    def GetConnections(him):
        return list(him.GetConnections())
        
    def GetChildren(him):
        node = him.GetNode()
        if node is not None:
            return [n.GetObject() for n in node.GetChilds()]
        
    def GetAppears(him):
        return list(him.GetAppears())

    @destructive
    def ModifyMetamodel(him, command, modificationBundles):
        bundleList = literal_eval(modificationBundles)
        bundleObjects = CModificationBundleFactory.CreateFromList(bundleList)

        node = him.GetNode()
        if node.IsModifiedMetamodelRoot():
            allBundles = IElementObject.__GetModificationBundles(node.GetMetamodel())
            for b in bundleObjects:
                if b.GetName() in allBundles:
                    raise PluginInvalidMethodParameters(him.GetUID(),
                        "Modification bundle with name %s already exists" % b.GetName())

        cmd = CApplyModificationBundlesCommand(node, bundleObjects)
        command.Execute(cmd)

    @destructive
    def RevertModifications(him, command, modificationBundles):
        bundleList = literal_eval(modificationBundles)
        node = him.GetNode()
        if not node.IsModifiedMetamodelRoot():
            raise PluginInvalidMethodParameters(him.GetUID(), "This element does not have any modifications defined")

        allBundles = IElementObject.__GetModificationBundles(node.GetMetamodel())
        bundleObjects = []
        for name in bundleList:
            if name not in allBundles:
                raise PluginInvalidMethodParameters(him.GetUID(), "Unknown bundle %s" % name)

            bundle = allBundles[name]

            bundleObjects.append(bundle)

        cmd = CRemoveModificationBundlesCommand(him.GetNode(), bundleObjects)
        command.Execute(cmd)
    
    @destructive
    def ConnectWith(him, command, other, connectionType):
        cmd = CCreateConnectionObjectCommand(him, other, connectionType)
        command.Execute(cmd)
        return cmd.GetConnectionObject()


    @destructive
    def CreateDiagram(him, command, diagramType):
        cmd = CCreateDiagramCommand(diagramType, him.GetNode())
        command.Execute(cmd)
        return cmd.GetDiagram()
    
    @destructive
    def CreateChildElement(him, command, elementType):
        cmd = CCreateElementObjectCommand(elementType, him.GetNode())
        command.Execute(cmd)
        return cmd.GetElementObject()
    
    @destructive
    def ShowIn(him, command, diagram):
        if diagram.HasElement(him):
            raise PluginInvalidMethodParameters(him.GetUID(), "element is already shown on given diagram")
        
        cmd = CShowElementCommand(him, diagram)
        command.Execute(cmd)
        return cmd.GetElementVisual()

    @classmethod
    @not_interface
    def __GetModificationBundles(cls, metamodel):
        return {b.GetName(): b for b in metamodel.GetModificationBundles()}
