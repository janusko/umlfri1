class CMetamodelModification:

    def __init__(self, objectTypeMappings):
        self.objectTypeMappings = objectTypeMappings

    def Apply(self):
        for type, element in self.objectTypeMappings:
            element.SetType(type)
