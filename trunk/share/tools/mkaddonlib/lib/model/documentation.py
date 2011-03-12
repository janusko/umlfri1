class Documentation(str):
    def indent(self, indentation, indentFirstLine = False, char = ' '):
        indent = char * indentation
        ret = ('\n' + indent).join(self.split('\n'))
        
        if indentFirstLine:
            ret = indent + ret
        
        return Documentation(ret)
