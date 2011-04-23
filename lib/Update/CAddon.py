class CAddon(object):
	def __init__(self,url,uri,version=None):	#(url=string,uri=string,version=CVersion)
		self.__uri = []
		self.__version = []
		self.__url = url
		self.__uri.append(uri)
		self.__version.append(version)
	
	def GetUrl(self):
		return self.__url
	
	def GetUri(self):
		return self.__uri

	def GetVersion(self):
		return self.__version
	
	def AppendUri(self,uri):
		self.__uri.append(uri)
	
	def AppendVersion(self,version):
		self.__version.append(version)
