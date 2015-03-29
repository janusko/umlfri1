class CMetamodelModification:

    def __init__(self, objectTypeMappings):
        self.objectTypeMappings = objectTypeMappings

    def __iter__(self):
        return self.objectTypeMappings.iteritems()

    def GetTypeForObject(self, object):
        return self.objectTypeMappings[object]

    def Apply(self):
        for object, type in self.objectTypeMappings.iteritems():
            object.SetType(type)
