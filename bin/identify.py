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
	working = string.lower()
	words = working.split()
	
	
	#JAVA
	jre = ['java', 'runtime', 'environment']
	jdk = ['java', 'development', 'kit']
	if set(jre).issubset(words):
		string = 'oracle jre'
	if set(jdk).issubset(words):
		string = 'oracle jdk'

	#MICROSOFT
	if '.NET' in words and 'Update' not in words:
		string = 'microsoft .net framework'
	
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
	output = open('../id.txt', 'w')
	junk = open('../no_id.txt', 'w')
	#jsonloot = open('../jsonloot.txt', 'w')
	association = {}
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
		
		output.write(app + '\tApplication Identified as:\t' + name + '\n')
		output.write('--------------------\n')
		#json.dump(association, jsonloot)
	output.close()
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
	
