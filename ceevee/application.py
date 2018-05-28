class vulnerability:
	def __init__(self, cve, url, summary, cvss, vuln_versions):
		self.cve = cve
		self.summary = summary
		self.cvss = cvss
		self.vuln_versions = vuln_versions
		self.url = url
		
	def getCve(self):
		return self.cve
		
	def getSummary(self):
		return self.summary
		
	def getCvss(self):
		return self.cvss
	
	def getVuln_versions(self):
		return self.vuln_versions
		
	def getUrl(self):
		return self.url
		
class application:
	def __init__(self, name, version, server):
		self.name = name
		self.servers = [server]
		self.versions = [version]
		self.possiblevendors = []
		self.vulnerabilities = []
		self.vulnvers = []
		self.vendors = []
		self.productname = ''
		
	def getName(self):
		return self.name
	
	def getProductname(self):
		return self.productname
	def setProductname(self, productname):
		self.productname = productname
		
	def getServers(self):
		return self.servers
	def addServer(self, server):
		self.servers.append(server)
	
	def getVersions(self):
		return self.versions
	def setVersion(self, version):
		self.versions.append(version)
	def setVersions(self, versions):
		self.versions = self.versions + versions
		
	def getVendors(self):
		return self.vendors
	def addVendor(self, vendor):
		self.vendors.append(vendor)
		
	def getPossiblevendors(self):
		return self.possiblevendors
	def addPossiblevendor(self, vendor):
		self.possiblevendors.append(vendor)
	def setPossiblevendors(self, vendors):
		self.possiblevendors = self.possiblevendors + vendors
		
	def addVulns(self, vuln_list):
		self.vulnerabilities = self.vulnerabilities + vuln_list
	def getVulns(self):
		return self.vulnerabilities
		
	def getVulnvers(self):
		return self.vulnvers
	def setVulnvers(self, vers):
		self.vulnvers = vers
		