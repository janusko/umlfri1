from lib.Depend.libxml import etree

from lib.lib import XMLEncode, Indent
from lib.Exceptions.UserException import *
import os.path
from lib.Distconfig import SCHEMA_PATH, USERDIR_PATH
import datetime
from lib.consts import RECENTFILES_NAMESPACE
from lib.Base import CBaseObject

xmlschema_doc = etree.parse(os.path.join(SCHEMA_PATH, "recentfiles.xsd"))
xmlschema = etree.XMLSchema(xmlschema_doc)


class CRecentFiles(CBaseObject):
    def __init__(self):
        self.filename = os.path.join(USERDIR_PATH, 'RecentFiles.xml')
        
        self.files = []
        self.LoadRecentFiles()

    
    def GetRecentFiles(self):
        for i in self.files:
            yield i
    
    def RemoveFile(self, file):
        for id, (f,d) in enumerate(self.files):
            if f == file:
                del self.files[id]
                return
    
    def AddFile(self, file):
        file = os.path.abspath(file)
        self.RemoveFile(file)
        self.files.insert(0,(file,datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")))
    
    def RecheckFiles(self):
        toRemove = []
        for filename, filedate in self.files:
            if not os.path.exists(filename):
                toRemove.append(filename)
        for filename in toRemove:
            self.RemoveFile(filename)

    def LoadRecentFiles(self):
        try:
            tree = etree.parse(self.filename)     #try to open and parse recentfile.xml file
        except:
            return
        
        root = tree.getroot()
        #xml (recentfiles.xml) file is validate with xsd schema (recentfile.xsd)
        if not xmlschema.validate(root):
            raise XMLError(xmlschema.error_log.last_error)

        for file in root.getchildren():
            if os.path.exists(file.get("name")):
                self.files.append((file.get("name"),file.get("date")))

    def SaveRecentFiles(self):
        root = etree.XML('<RecentFiles xmlns="http://umlfri.kst.fri.uniza.sk/xmlschema/recentfiles.xsd"></RecentFiles>')
        
        for name, date in self.files:
            root.append(etree.Element(RECENTFILES_NAMESPACE+"File", name=name, date=date))  #namespace {xxx} is required

        #xml tree is validate with xsd schema (recentfile.xsd)
        if not xmlschema.validate(root):
            raise XMLError(xmlschema.error_log.last_error)
        
        #make human-friendly tree
        Indent(root)
        
        #save Recent File Tree
        f = open(self.filename, 'w')
        f.write('<?xml version="1.0" encoding="utf-8"?>\n'+etree.tostring(root, encoding='utf-8'))
        f.close()
        