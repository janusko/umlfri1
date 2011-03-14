from .baseContainer import BaseContainer

class Namespace(BaseContainer):
    def __init__(self, name, parent):
        BaseContainer.__init__(self, name, parent)
    
    @property
    def descendants(self):
        for child in self.children:
            yield child
            if isinstance(child, Namespace):
                for grandDescendant in child.descendants:
                    yield grandDescendant
