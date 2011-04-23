class CUpdate(object):
	def __init__(self):
		self.__ListOfAddons = []
		
	def Update(self,List):
		self.__ListOfAddons = List
		self.Vypis()
		self.Simplify()
		self.Vypis()
		self.ParseXML()
		self.ParseHTML()	
	
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

	def ParseXML(self):
		for i in range (0,len(self.__ListOfAddons)):
			try:
				xml =  urllib.urlopen(self.__ListOfAddons[i].GetUrl()).read()
				context = etree.iterparse(StringIO(xml))
				try:				
					for action, elem in context:
						if elem.tag == 'description' and elem.text!=None:
							self.__ListOfAddons[i].AddDescription(elem.text)
				except SyntaxError:
					self.__ListOfAddons[i].AddDescription(None)				
					print 'Incorrect XML format'					
			except IOError:
				self.__ListOfAddons[i].AddDescription(None)				
				print 'Name or service not known'
		print '-----------------------------'
		print 'Descriptions:'		
		for i in range (0,len(self.__ListOfAddons)):
			print self.__ListOfAddons[i].GetDescription()

	def napln(self,x,html):
		try: 
			data = html.find_class(x)[0].text_content()
		except IndexError:
			data = ""
		return data
	
	def ParseHTML(self):
		for i in range (0,len(self.__ListOfAddons)):
			for j in range (0,len(self.__ListOfAddons[i].GetDescription())):
				try:
					html = fromstring(self.__ListOfAddons[i].GetDescription()[j])
					self.__ListOfAddons[i].SetDescription(j,self.napln(URI,html),self.napln(URL,html),self.napln(SYS,html),self.napln(VER,html),self.napln(ARCH,html))
				except KeyError:
					pass
				except TypeError:
					pass
		print '-----------------------------'
		print 'Data z descriptions:'
		for i in range (0,len(self.__ListOfAddons)):
			for j in range (0,len(self.__ListOfAddons[i].GetDescription())):
				print self.__ListOfAddons[i].GetDescription()[j]
