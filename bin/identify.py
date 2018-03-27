import re, json, difflib
import urllib.request
spaces = re.compile(' ')
plus = re.compile('\+')
version = re.compile(r'\s[\S]*[\d]+.', re.DOTALL)

def closest(products, name, app_list):
	highest = 0
	value = ''
	
	for product in products:
		current = difflib.SequenceMatcher(None, name, product).ratio()
		if current > highest:
			value = product
			highest = current
			
	if highest < .7:
		return ''
	return value
	
def clean_string(string):
	#JAVA
	jre = ['java', 'runtime', 'environment']
	jdk = ['java', 'development', 'kit']
	words = string.split()
	if jre in words:
		string = 'oracle jre'
		print('jre')
	if jdk in words:
		string = 'oracle jdk'
		print('jdk')

	#MICROSOFT
	if '.NET' in words and 'Update' not in words:
		string = 'microsoft .net framework'
	
	#VERSION NUMBERS
	match = version.search(string)
	if match:
		string = string[:match.start()]
	"""
	#BRACKETS
	string = bracs.sub('', string)
	"""
	if len(words) > 1:
		#remove the vendor name?
		pass
	
	return string
	
def optimize(string):
	#optimization rules to find closest match via API
	#optimized = plus.sub('%2b', string)
	optimized = spaces.sub('_', string)
	optimized = urllib.parse.quote_plus(optimized)
	optimized = optimized.lower()
	return optimized
	

def determine_product(application_list):
	output = open('../loot.txt', 'w')
	output.write('IDENTIFIED APPLICATION\n')
	output.write('++++++++++++++++++++++\n')
	for app in application_list:
		products = []
		vendors = []
		for vendor in application_list[app]:
			tmp = json.load(open('../files/' + vendor + '_productlist.txt'))
			products = products + tmp
			vendors.append(vendor)
		appready = clean_string(app)
		appready = optimize(appready)
		name = closest(products, appready, vendors)
		if name == '':
			continue
		output.write(app + '\tApplication Identified as:\t' + name + '\n')
		output.write('--------------------\n')
	output.close()
	
	
def get_version(application_list):
	pass
	"""
	#json_input = json.load(open('json_MList.txt'))
	#vendorlist = json_input['vendors']
	output = open('tmp.txt', 'w')
	#check if vendor is in sw?
	for line in sw_input:
		vendor_match = []
		software = line[:-1]
		if addriver.match(software):
			continue
		software = preparse(software)
		for vendor in vendorlist:
			q = re.compile(r'(\b|^)'+vendor+r'\b', re.IGNORECASE)
			if q.search(software):
				vendor_match.append(vendor)
		if len(vendor_match) > 0:
			optimized = optimize(software)
			products = []
			
			TODO
			remove vendor name before comparing ratio
			disregard low ratio results
			convert '#' to %23
			
			for each in vendor_match:
				url = 'http://cve.circl.lu/api/browse/' + each
				result = requests.get(url, headers=headers)
				if result.status_code != 200:
					print('request failed' + url)
				else:
					tmp = json.loads(result.content.decode('utf-8'))
					products = products + tmp['product']
			sw_list.append(application(software, closest(products, optimized)))
			
	output = open('best_guess.txt', 'w')

	print('writing')
	for sw in sw_list:
		output.write(sw.get_vendor() + sw.get_name() + '\n')
	output.close()
	"""