class CUpdateRequest(object):
    def __init__(self,url,uri,version=None):
        self.__data = {'url': url, 'uri': uri, 'ver': version, 'des': []}
        self.__RSSVersion = self.__data['ver']
        self.__RSSUrl = ''
        self.__RSSUri = ''

    def GetData(self):
        return self.__data

    def GetUrl(self):
        return self.__data['url']

    def GetUri(self):
        return self.__data['uri']

    def GetVersion(self):
        return self.__data['ver']

    def GetDescription(self):
        return self.__data['des']

    def SetDescription(self,x):
        self.__data['des'] = x

    def AddDescription(self,x):
        self.__data['des'].append(x)

    def SetRSSVersion(self,x):
        self.__RSSVersion = x

    def GetRSSVersion(self):
        return self.__RSSVersion

    def SetRSSUrl(self,x):
        self.__RSSUrl = x

    def GetRSSUrl(self):
        return self.__RSSUrl
	
    def SetRSSUri(self,x):
        self.__RSSUri = x

    def GetRSSUri(self):
        return self.__RSSUri
