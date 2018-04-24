import re, json, difflib
import urllib.request

#REGEX
spaces = re.compile(' ')
plus = re.compile('\+')
rversion = re.compile(r'\s[\S]*[\d]+.', re.DOTALL) #Quick and dirty
version = re.compile(r'\s[\S]*[\d][\S]*')
vversion = re.compile('\S*\d\S*' + '|' + '\(.\)' + '|' + '\S*\d\S*', re.DOTALL); #Internal version numbers
up = re.compile('.*'+'\s'+'update'+'\s'+'.*', re.IGNORECASE); #Is an update
java = re.compile('.*java.*', re.IGNORECASE); #Java program?

def closest(products, name, app_list):
	highest = 0
	value = ''
	
	for product in products:
		current = difflib.SequenceMatcher(None, name, product).ratio()
		if current > highest:
			value = product
			highest = current
	"""
	It should be noted that when string operations such as optimize and clean are performed, vendor names may be removed as garbage values. So expect that they may not be found. 
	"""
	
	for vendor in app_list:
		namelist = name.split('_')
		if vendor in namelist:
			namelist.remove(vendor)
			mod_name = '_'.join(namelist)
			for product in products:
				current = difflib.SequenceMatcher(None, mod_name, product).ratio()
				if current > highest:
					value = product
					highest = current
				
	
	#Finished comparisons, return result if we are satisfied
	if highest < .8:
		return ''
	return value
	
#A rougher way to clean the string, just strip anything that might not be a product name. 
def cleann_string(string):
	#VERSION NUMBERS
	match = rversion.search(string)
	if match:
		string = string[:match.start()]
	return string
	'''
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
	'''
	
#Clean the string precisely, remove version numbers, architecture information, etc...
def clean_string(string):
	'''
	#JAVA
	jre = ['java', 'runtime', 'environment']
	jdk = ['java', 'development', 'kit']
	lower = string.lower()
	words = lower.split()
	if jre in words:
		string = 'oracle jre'
		print('jre')
	if jdk in words:
		string = 'oracle jdk'
		print('jdk')

	#MICROSOFT
	if '.NET' in words and 'Update' not in words:
		string = 'microsoft .net framework'
	'''
	#VERSION NUMBERS
	match = version.search(string)
	if match:
		string = string[:match.start()] + string[match.end():]
		#string[:match.start()]
	"""
	#BRACKETS
	string = bracs.sub('', string)
	"""
	#if len(words) > 1:
		#remove the vendor name?
	#	pass
	
	return string
	
def optimize(string):
	#optimization rules to find closest match via API
	#optimized = plus.sub('%2b', string)
	optimized = spaces.sub('_', string)
	optimized = urllib.parse.quote_plus(optimized)
	optimized = optimized.lower()
	return optimized
	

def determine_product(application_list):
	#output = open('../loot.txt', 'w')
	junk = open('../no_id.txt', 'w')
	jsonloot = open('../jsonloot.txt', 'w')
	association = {}
	#output.write('IDENTIFIED APPLICATIONS\n')
	#output.write('++++++++++++++++++++++\n')
	for app in application_list:
		products = []
		for vendor in application_list[app]:
			tmp = json.load(open('../files/' + vendor + '_productlist.txt'))
			products = products + tmp
		appready = clean_string(app)
		appready = optimize(appready)
		name = closest(products, appready, application_list[app])
		if name == '':
			appready = cleann_string(app)
			appready = optimize(appready)
			name = closest(products, appready, application_list[app])
			if name == '':
				junk.write(app + '\n')
				application_list[app] = ''
				continue
		
		association[app] = name
		for vendor in application_list[app]:
			if name in json.load(open('../files/' + vendor + '_productlist.txt')):
				application_list[app] = vendor
				break
		
		#output.write(app + '\tApplication Identified as:\t' + name + '\n')
		#output.write('--------------------\n')
		json.dump(association, jsonloot)
	#output.close()
	junk.close()
	return association
	
#Given a name, extract the possible version numbers.
def determine_versions(associations):
	versions = {}
	for name, software in associations.items():
		versionlist = vversion.findall(name)
		versionliststr = [x.strip('()') for x in versionlist]
		versions[name] = versionliststr
	return versions
	
	"""
	#Is a Java program[ 0 update 0 --> 0u0]
	if up.search(string) and java.search(string):
		string = m.sub('u', string);
		vendor = 'oracle'
	"""
	
	
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