from lib.consts import USERGUI_PATH, USERGUI_NAMESPACE
from lib.Depend.etree import etree, HAVE_LXML,XMLSyntaxError
from lib.config import config
from lib.Exceptions.DevException import *
import os, os.path
from lib.lib import Indent


##if lxml.etree is imported successfully, we use xml validation with xsd schema
#if HAVE_LXML:
#    xmlschema_doc = etree.parse(os.path.join(config['/Paths/Schema'], "metamodel.xsd"))
#    xmlschema = etree.XMLSchema(xmlschema_doc)
types = {
    '/frmMain/form/height-request':int,
    '/frmMain/form/width-request':int,
    '/frmMain/hpaRight/position':int,
    '/frmMain/vpaRight/position':int,
}

class CUserGui(object):
    
    def __init__ (self,app):
        self.app = app
        self.LoadConfig()
        #self.ApplyConfig()
        
    def __recursive(self,root, path,cfg):    
        for child in root:
            name = path+child.tag.split('}')[1]
            if len(child):
                self.__recursive(child, name+'/', cfg)
            elif child.text is None:
                cfg[name] = types.get(name, unicode)('')
            else:
                cfg[name] = types.get(name, unicode)(child.text)
                
    def LoadConfig(self):
        """
        Load an XML file under given path
        """
        try:
            self.file = config['/Paths/UserGui']
            if os.path.isfile(self.file):
                tree = etree.XML(open(self.file).read())
                print "nacitany etree"
#                if HAVE_LXML:
#                    if not self.xmlschema.validate(tree):
#                        raise ConfigError, ("XMLError", self.xmlschema.error_log.last_error)
                self.cfg = {}
                self.__recursive(tree,'/',self.cfg)
                print self.cfg
                
        except (XMLSyntaxError, ConfigError):
            print 'WARNING: dopisat nieco!!!!!!'
            raise
            
    def SaveConfig(self):
        """
        Save changes to UserGui config XML file
        """
        self.UpdateConfig()
        out = {}
        save = {'UserGui':out}
        f = file(self.file,'w')
        
        def save(root = save['UserGui'], node = None, level = 1):
            for part, val in root.iteritems():
                newNode = etree.Element('{%s}%s'%(USERGUI_NAMESPACE, part))
                if isinstance(val, dict):
                    save(val, newNode, level+1)
                else:
                    newNode.text = unicode(val)
                node.append(newNode)
        
        for path, val in self.cfg.iteritems():
            tmp = out
            path = path.split('/')
            for part in path[1:-1]:
                tmp2 = tmp.setdefault(part, {})
                if not isinstance(tmp2, dict):
                    tmp2 = tmp[part] = {}
                tmp = tmp2
            tmp[path[-1]] = val
        
        rootNode = etree.XML('<UserGui xmlns="%s"></UserGui>'%USERGUI_NAMESPACE)
        save(node = rootNode)
        
#        #xml tree is validate with xsd schema (recentfile.xsd)
#        if HAVE_LXML:
#            if not self.xmlschema.validate(rootNode):
#                raise ConfigError, ("XMLError", self.xmlschema.error_log.last_error)
        
        #make human-friendly tree
        Indent(rootNode)
        
        print>>f, '<?xml version="1.0" encoding="utf-8"?>'
        print>>f, etree.tostring(rootNode, encoding='utf-8')
        
    def ApplyConfig(self):
        for path in types:
            path2 = path.split('/')
            act = self.app.GetWindow(path2[1])
            for part in path2[2:-1]:
                act = getattr(act, part)
            print act, self.cfg[path]
            act.set_property(path2[-1],self.cfg[path])
        

        #frmMain = self.app.GetWindow('frmMain')
        #print frmMain.vpaRight.get_position()
        #print frmMain.hpaRight.get_position()
        #frmMain.vpaRight.set_position(self.cfg['/frmMain/vpaRight/position'])
        #frmMain.hpaRight.set_position(self.cfg['/frmMain/hpaRight/position'])
        
    def UpdateConfig(self):
        
        for path in types:
            path2 = path.split('/')
            act = self.app.GetWindow(path2[1])
            for part in path2[2:-1]:
                act = getattr(act, part)
            self.cfg[path] = act.get_property(path2[-1])
        

