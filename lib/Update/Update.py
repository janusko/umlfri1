from lxml import etree
from cStringIO import StringIO
from lxml.html import fromstring
import urllib
import platform

from lib.datatypes import CVersion
from Addon import CAddon

#--constants-----------------------------------------------------------
URI="Curi"
URL="Curl"
SYS="Csystem"
ARCH="Carchitecture"
VER="Cversion"
#----------------------------------------------------------------------
class CUpdate(object):
    def __init__(self):
        self.__LOA = []
            
    def Update(self,List):
        self.__LOA = List
        self.__ParseXML()
        self.__ParseHTML()    
        return self.__Download()     

    def __ParseXML(self):
        List = [] 
        y = False      
        for i in self.__LOA:
            for j in self.__LOA:
                if i.GetUri()==j.GetUri() and j.GetDescription()!=[]:
                    i.SetDescription(j.GetDescription())
                    y = True
                    break   
            if not y:
                try:
                    xml = urllib.urlopen(i.GetUrl()).read()
                    context = etree.iterparse(StringIO(xml))
                    try:                    
                        for action, elem in context:
                            if elem.tag.find('summary')!=-1 and elem.text!=None:
                                i.AddDescription(elem.text)          
                            if elem.tag.find('description')!=-1 and elem.text!=None:
                                i.AddDescription(elem.text)
                    except SyntaxError:
                        pass            
                except IOError:
                    pass   

    def __parse(self,x,html):
        try: 
            data = html.find_class(x)[0].text_content()
        except IndexError:
            data = ""
        return data

    def __ParseHTML(self):
        for i in self.__LOA:
            for j in range(0,len(i.GetDescription())):
                try:
                    html = fromstring(i.GetDescription()[j])
                    if self.__parse(URI,html)!='' and self.__parse(URL,html)!='' and self.__parse(VER,html)!='':
                        if self.__parse(URI,html)==i.GetUri():
                            if self.__parse(SYS,html)=='' or platform.system()==self.__parse(SYS,html):
                                if self.__parse(ARCH,html)=='' or platform.architecture()[0]==self.__parse(ARCH,html):
                                    try:
                                        if i.GetRSSVersion().GetVersion() < CVersion(self.__parse(VER,html)).GetVersion():
                                            i.SetRSSVersion(CVersion(self.__parse(VER,html)))  
                                            i.SetRSSUrl(self.__parse(URL,html))
                                    except AttributeError: 
                                        i.SetRSSVersion(CVersion(self.__parse(VER,html)))  
                                        i.SetRSSUrl(self.__parse(URL,html)) 
                except KeyError:
                    pass        
    
    def __Download(self):
        List = []
        for i in self.__LOA:
            if i.GetRSSUrl()!='':
                try:
                    netfile = urllib.urlopen(i.GetRSSUrl())
                    data = netfile.read()
                    ramfile = StringIO(data)
                    List.append(ramfile)
                except IOError:
                    List.append(None)
            else:
                List.append(None)
        return List
