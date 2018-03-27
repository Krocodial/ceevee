class application:
	def __init__(self, name, vendor):
		self.name = name
		self.vendors = []
		self.vendors.append(vendor)
		
	def get_name(self):
		return self.name
	
	def get_vendors(self):
		return self.vendors
		
	def add_vendor(self, vendor):
		self.vendors.append(vendor)