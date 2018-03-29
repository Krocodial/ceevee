class application:
	def __init__(self, name, version, server):
		self.name = name
		self.productname = ''
		self.versions = self.servers = []
		self.versions.append(version)
		self.servers.append(server)
		self.cves = []
		self.cvss = 0
		self.vendor = ''
			
	def getName(self):
		return self.name
	
	def setProductName(self, name):
		self.productname = name
	def getProductName(self):
		return self.productname
	
	def getVersions(self):
		return self.versions	
	def addVersions(self, version):
		self.versions = self.versions + version
	
	def getServers(self):
		return self.servers		
	def addServer(self, server):
		self.servers.append(server)
	
	def getCves(self):
		return self.cves
	def addCve(self, cve):
		self.cves.append(cve)
		
	def getCvss(self):
		return self.cvss
	def setCvss(self, cvss):
		self.cvss = cvss
		
	def getVendor(self):
		return self.vendor	
	def setVendor(self, vendor):
		self.vendor = vendor