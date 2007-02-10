import xml.dom.minidom
import consts
import os.path
import os

class CConfig:
    file = None
    def __init__(self, file):
        self.Clear()
        self.Load(file)
        if not os.path.isdir(self['/Paths/UserDir']):
            os.mkdir(self['/Paths/UserDir'])
        self.original = self.cfgs.copy()
        if os.path.isfile(self['/Paths/UserConfig']):
            self.Load(self['/Paths/UserConfig'])
        self.file = self['/Paths/UserConfig']
        #~ if userconfig is not None:
            #~ self.original = self.cfgs.copy()
            #~ if os.path.isfile(userconfig):
                #~ self.load(userconfig)
            #~ self.file = userconfig
        #~ else:
            #~ self.file = file
    
    def __del__(self):
        self.Save()
    
    def Clear(self):
        self.cfgs = {}
        self.original = self.cfgs
        self.__getitem__ = self.cfgs.__getitem__
        self.__setitem__ = self.cfgs.__setitem__
        self.__contains__ = self.cfgs.__contains__
    
    def Load(self, root, path = None):
        if isinstance(root, (str, unicode)):
            root = xml.dom.minidom.parse(root).documentElement
        if path is None:
            path = ''
        else:
            path += '/'+root.tagName
        text = ''
        for i in root.childNodes:
            if i.nodeType == i.TEXT_NODE:
                text += i.data.decode('unicode_escape')
            if i.nodeType not in (i.ELEMENT_NODE, i.DOCUMENT_NODE):
                continue
            if i.tagName == 'Include':
                if i.hasAttribute('what'):
                    if i.getAttribute('what') == 'app_path':
                        text += consts.ROOT_PATH
                        continue
                elif i.hasAttribute('path'):
                    text += self.cfgs[i.getAttribute('path')]
                    continue
            self.cfgs[path+'/'+i.tagName] = self.Load(i, path)
        if root.hasAttribute('type'):
            type = root.getAttribute('type')
            if type == 'int':
                text = int(text)
            elif type == 'float':
                text = float(text)
            elif type == 'bool':
                text = text.lower() in ('0', 'f', 'no', 'false')
            elif type == 'path':
                text = os.path.abspath(os.path.expanduser(text))
                if os.path.isdir(text):
                    text += os.sep
            return text
        else:
            return text
    
    def Save(self):
        out = {}
        save = {'Config': out}
        
        f = file(self.file, 'w')
        
        def XMLEncode(val):
            ret = repr(val)
            if isinstance(val, str):
                ret = ret[1:-1]
            elif isinstance(val, unicode):
                ret = ret[2:-1]
            return ret.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('<', '&gt;').replace('"', '&quot;')
        
        def save(root = save, level = 0):
            for part, val in root.iteritems():
                if isinstance(val, dict):
                    print>>f, ' '*(level*4)+'<%s>'%part
                    save(val, level+1)
                    print>>f, ' '*(level*4)+'</%s>'%part
                else:
                    print>>f, ' '*(level*4)+'<%s>%s</%s>'%(part, XMLEncode(val), part)
        
        for path, val in self.cfgs.iteritems():
            if val != self.original.get(path, None):
                tmp = out
                path = path.split('/')
                for part in path[1:-1]:
                    tmp = tmp.setdefault(part, {})
                tmp[path[-1]] = val
        
        save()

config = CConfig(consts.MAIN_CONFIG_PATH)
