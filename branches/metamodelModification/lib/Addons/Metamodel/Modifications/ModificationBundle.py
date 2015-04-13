class CMetamodelModificationBundle(object):

    def __init__(self, name, elementModifications, domainModifications):
        self.name = name
        self.elementModifications = elementModifications
        self.domainModifications = domainModifications

    def GetName(self):
        return self.name

    def GetElementModifications(self):
        return self.elementModifications

    def GetDomainModifications(self):
        return self.domainModifications