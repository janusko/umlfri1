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
            ret = sentences.pop(0) + '.'
            while len(sentences) > 0 and sentences[0].startswith('FRI'):
                ret += sentences.pop(0) + '.'
            return ret
        else:
            return str(self)
