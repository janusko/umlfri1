class CAddon(object):
	def __init__(self,url,uri,version=None):	#(url=string,uri=string,version=CVersion)
		self.__url = url
		self.__uri = uri
		self.__version = version
	
	def GetUrl(self):
		return self.__url
	
	def GetUri(self):
		return self.__uri

	def GetVersion(self):
		return self.__version
