class CUpdateManager(object):
	def __init__(self):
		self.__data = []
		self.__ListOfAddons = []
		
	def Update(self,List):
		self.__ListOfAddons = List
		self.Vypis()
		self.Simplify()
		self.Vypis()
		#self.ParseXML(ListOfAddons[i].GetUrl())
		#self.ParseHTML()	
	
	def Vypis(self):
		for i in range (0,len(self.__ListOfAddons)):
			print 'URL:',self.__ListOfAddons[i].GetUrl()
			print 'Uri:',self.__ListOfAddons[i].GetUri()
			if self.__ListOfAddons[i].GetVersion() is not None:
				print 'Version:',self.__ListOfAddons[i].GetVersion()
			else: 
				print 'Version: N/A'
			print '-----------------------------'	
		print '-----------------------------'
			
	def Simplify(self):
		UrlList = []
		ShortList = []
		for i in range (0,len(self.__ListOfAddons)):
			if self.__ListOfAddons[i].GetUrl() not in UrlList:
				UrlList.append(self.__ListOfAddons[i].GetUrl())
				ShortList.append(self.__ListOfAddons[i])
			else:
				x = UrlList.index(self.__ListOfAddons[i].GetUrl())
				ShortList[x].AppendUri(self.__ListOfAddons[i].GetUri()[0])
				ShortList[x].AppendVersion(self.__ListOfAddons[i].GetVersion()[0])
		self.__ListOfAddons = ShortList

	def ParseXML(self,url):
		xml =  urllib.urlopen(url).read()
		#tree = etree.parse(StringIO(xml))
		context = etree.iterparse(StringIO(xml))
		desc = []
		for action, elem in context:
			if elem.tag == "description" and elem.text!=None:
				desc.append(elem.text)
			
		self.__descriptions = desc

	def napln(self,x,html):
		try: 
			data = html.find_class(x)[0].text_content()
		except IndexError:
			data = ""
		return data
	
	def ParseHTML(self):
		books = []	
		for i in range (0,len(self.__descriptions)):
			try:
				#v = htmlFile[i]["description"]
				html = fromstring(self.__descriptions[i])
				books.append(self.napln(URI,html))	
				books.append(self.napln(URL,html))
				books.append(self.napln(SYS,html))
				books.append(self.napln(VER,html))
				books.append(self.napln(ARCH,html))
				#if (book_dict[URI]!="" and book_dict[URL]!="" and book_dict[VER]!=""):
				#	books.append(book_dict)
				self.__data.append(books)
				books = []
			except KeyError:
				pass

	def GetData(self):
		return self.__data
