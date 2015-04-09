class CMetamodelModificationBundle(object):

    def __init__(self, name, elementModifications):
        self.name = name
        self.elementModifications = elementModifications

    def GetName(self):
        return self.name

    def GetElementModifications(self):
        return self.elementModifications