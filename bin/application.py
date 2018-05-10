class vuln:
	def __init__(self, cve, url, summary, cvss):
		self.cve = cve
		self.url = url
		self.summary = summary
		self.cvss = cvss


class application:
	def __init__(self, name, version, server):
		self.name = name
		self.productname = ''
		self.servers = []
		self.versions = []
		self.versions.append(version)
		self.servers.append(server)
		self.cves = []
		self.cvss = 0
		self.vendor = ''
		self.vulnerabilities = []
			
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
		
	def addVuln(self, cve, url, summary, cvss):
		self.cvss = self.cvss + cvss
		self.vulnerabilities = self.vulnerabilities.append(vuln(cve, url, summary, cvss))
	def getVulns(self):
		return self.vulnerabilities
		