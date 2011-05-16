from lib.Depend.libxml import etree, html
from cStringIO import StringIO
import urllib
import platform

from lib.datatypes import CVersion
from UpdateRequest import CUpdateRequest
from UpdateResponse import CUpdateResponse

#--constants-----------------------------------------------------------
URI="Curi"
URL="Curl"
SYS="Csystem"
ARCH="Carchitecture"
VER="Cversion"
#----------------------------------------------------------------------
class CUpdateManager(object):
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
                for k in i.GetUri():
					if k in j.GetUri() and j.GetDescription()!=[]:
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

    def __parse(self,x,text):
        try: 
            data = text.find_class(x)[0].text_content()
        except IndexError:
            data = ""
        return data

    def __ParseHTML(self):
        for i in self.__LOA:
            for j in range(0,len(i.GetDescription())):
                try:
                    text = html.fromstring(i.GetDescription()[j])
                    if self.__parse(URI,text)!='' and self.__parse(URL,text)!='' and self.__parse(VER,text)!='':
                        if self.__parse(URI,text) in i.GetUri():
                            if self.__parse(SYS,text)=='' or platform.system()==self.__parse(SYS,text):
                                if self.__parse(ARCH,text)=='' or platform.architecture()[0]==self.__parse(ARCH,text):
                                    try:
                                        if i.GetRSSVersion() < CVersion(self.__parse(VER,text)):
                                            i.SetRSSVersion(CVersion(self.__parse(VER,text)))  
                                            i.SetRSSUrl(self.__parse(URL,text))
                                            i.SetRSSUri(self.__parse(URI,text))
                                    except AttributeError: 
                                        i.SetRSSVersion(CVersion(self.__parse(VER,text)))  
                                        i.SetRSSUrl(self.__parse(URL,text)) 
                                        i.SetRSSUri(self.__parse(URI,text))
                except KeyError:
                    pass        
    
    def __Download(self):
        List = []
        for i in self.__LOA:
            if i.GetRSSUrl()!='':
                try:
                    netfile = urllib.urlopen(i.GetRSSUrl())#prava, server, port,prerusenie spojenia, neexist. subur
                    data = netfile.read()
                    ramfile = StringIO(data)
                    new = CUpdateResponse(ramfile,i.GetRSSUri())
                    List.append(new)
                except IOError:
                    pass#List.append(None)
            else:
                pass#List.append(None)
        return List
