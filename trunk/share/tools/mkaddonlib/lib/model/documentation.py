class Documentation(str):
    def indent(self, indentation, indentFirstLine = False, char = ' '):
        indent = char * indentation
        ret = ('\n' + indent).join(self.split('\n'))
        
        if indentFirstLine:
            ret = indent + ret
        
        return Documentation(ret)
    
    @property
    def firstSentence(self):
        if '.' in self:
            sentences = self.split('.')
            return sentences[0] + '.'
        else:
            return str(self)
