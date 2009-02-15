class CChildrenEvalWrapper(object):
    def __init__(self, node):
        self.__node = node
    
    def __iter__(self):
        for child in self.__node.GetChilds():
            yield {
                'icon': child.GetObject().GetType().GetIcon(),
                'name': child.GetObject().GetName()
            }
