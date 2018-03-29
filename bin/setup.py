import re, os, csv, json, requests, urllib.request
from application import application

spaces = re.compile(' ')
plus = re.compile('\+')
version = re.compile(r'\s[\S]*[\d]+.', re.DOTALL)
addriver = re.compile('^XA650.', re.DOTALL)
bracs = re.compile('[(].[)]', re.DOTALL)

def parse_csv(name):
	try:
		input = csv.reader(open(name, newline=''))
		list = []
		names = []
		for line in input:
			break
		counter = 0
		row_count = sum(1 for i in csv.reader(open(name)))
		itera = int(row_count/100)
		for line in input:
			if not counter % itera:
				print('\rProcessed: ' + str(counter//itera) + '%', end='')
			counter = counter + 1
			
			if len(line) < 3:
				break
			server = line[0]
			name = line[1]
			
			if addriver.match(name): #useless drivers
					continue
			version = line[2]
			flag = 1
			
			for obj in list:
				if obj.getName() == name and version not in obj.getVersions():
					obj.addServer(server)
					flag = 0
					break
			if flag:
				tmp = application(name, version, server)
				if name not in names:
					names.append(name)
				list.append(tmp)
		output = open('../files/shortlist.txt', 'w')
		json.dump(names, output)
		output.close()
		return list
		
	except Exception as e:
		print(e)
		print('Error \nPlease ensure you are entering the name of a csv file, and that the file is in the ~/files directory')
		exit()

def update(app_list, application_list, associations, versions):
	real_names = {}
	for app in app_list:
		name = app.getName()
		vendor = application_list[name]
		r_name = associations[name]
		app.setVendor(vendor)
		app.setProductName(r_name)
		app.addVersions(versions[name])
		if r_name not in real_names:
			real_names[r_name] = vendor
	return real_names
		
"""
Update our vendor list
"""
def pull_vendors():
	output = open('../files/vendors.txt', 'w')
	
	result = requests.get('https://cve.circl.lu/api/browse')
	if result.status_code != 200:
		print('There is something wrong with the API')
		exit()
	else:
		try:
			dic = json.loads(result.content.decode('utf-8'))
			vendors = dic['vendor']
			json.dump(vendors, output)
			output.close()
		except Exception as e:
			print(e)
			exit()
	
"""
Pulls products associated with the vendor and dumps to a text file
"""
def pull_products(vendor):
	result = requests.get('https://cve.circl.lu/api/browse/' + vendor)
	if result.status_code != 200:
		print("Are you sure that's a valid vendor? I couldn't grab the vendor's product list")
		exit()
	else:
		try:
			raw = json.loads(result.content.decode('utf-8'))
			products = raw['product']
			output = open('../files/' + vendor + '_productlist.txt', 'w')
			json.dump(products, output)
			output.close()
		except Exception as e:
			print(e)
			exit()
"""
Pre-parse so we can identify tricky vendors			
"""
def preparse(string):

	#JAVA
	jre = ['java', 'runtime', 'environment']
	jdk = ['java', 'development', 'kit']
	words = string.split()
	if jre in words:
		string = 'oracle jre'
	if jdk in words:
		string = 'oracle jdk'

	#MICROSOFT
	if '.NET' in words and 'Update' not in words:
		string = 'microsoft .net framework'
	"""	
	#VERSION NUMBERS
	match = version.search(string)
	if match:
		string = string[:match.start()]
		
	#BRACKETS
	string = bracs.sub('', string)
	
	if len(words) > 1:
		#remove the vendor name?
		pass
	"""
	return string
		
		
def find_vendors(application_list):
	vendors = json.load(open('../files/vendors.txt'))
	sw_input = json.load(open('../files/shortlist.txt'))

	vendorlist = []
	sw_products = []
	
	for line in sw_input:
		software = preparse(line)
		sw_products.append(software)

	for vendor in vendors:
		q = re.compile(r'(\b|^)' + vendor + r'\b', re.IGNORECASE)	
		for product in sw_products:
			if q.search(product):
				if product not in application_list:
					application_list[product] = [vendor]
				else:
					if vendor not in application_list[product]:
						application_list[product].append(vendor)
					
				if vendor not in vendorlist:
					vendorlist.append(vendor)
					
	#update vendors.txt, this saves us a lot of runtime
	vendor_output = open('../files/vendors.txt', 'w')
	json.dump(vendorlist, vendor_output)
	
	return vendorlist
	
	
def clean():
	pattern = re.compile('.productlist.txt')
	for f in os.listdir('../files/'):
		if re.search(pattern, f):
			os.remove(os.path.join('../files/', f))
	
	
	
	
	