import re, json, difflib, urllib.request, requests, datetime
from multiprocessing import Queue
from bs4 import BeautifulSoup

rversion = re.compile(r'\s[\S]*[\d]+.', re.DOTALL) #Quick and dirty
version = re.compile(r'\s[\S]*[\d][\S]*')
vversion = re.compile('[\S]*\d[\S]*')
spaces = re.compile(' ')
rpm = re.compile('REL')
java = re.compile('\d+\supdate\s\d+', re.IGNORECASE)
jav = re.compile('java', re.IGNORECASE)
bracks = re.compile(r'\( | \)')

cve_details_url = 'https://www.cvedetails.com/';
searchext = 'product-search.php?vendor_id=0&';

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'};


def closest(products, name, vendors, ratio):
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
	
	for vendor in vendors:
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
	if highest < ratio:
		return ''
	return value



def optimize(name):
	optimized = spaces.sub('_', name)
	optimized = urllib.parse.quote_plus(optimized)
	optimized = optimized.lower()
	return optimized

def java_check(obj):
	name = obj.getName()
	jdk = ['java', 'development', 'kit']
	tmp = name.split()
	if jav.search(name) and java.search(name):
		if set(jdk).issubset(tmp) or 'jdk' in tmp:
			obj.setProductname('jdk')
			obj.addPossiblevendor('oracle')
			#name = 'jdk'
		else:
			obj.setProductname('jre')
			obj.addPossiblevendor('oracle')
			#name = 'jre'
	return obj
	
def cleann_string(name):

	jdk = ['java', 'development', 'kit']
	tmp = name.lower()
	tmp = tmp.split()
	if jav.search(name) and java.search(name):
		if set(jdk).issubset(tmp) or 'jdk' in tmp or 'sdk' in tmp:
			name = 'jdk'
		else:
			name = 'jre'
	match = rversion.search(name)
	if match:
		name = name[:match.start()]
	return name
	
def clean_string(name):
	match = version.search(name)
	if match:
		name = name[:match.start()] + name[match.end():]
		#match = version.search(string)
		#print('cleaning')
	return name

def cleannn_string(name):
	name = bracks.sub('', name)
	return name
	
def determine_products(object_list, ratio, thorough):
	new_object_list = []
	output = open('../id.txt', 'w')
	junk = open('../no_id.txt', 'w')
	for app in object_list:
		oname = app.getName()
		#print(oname)
		products = []
		app = java_check(app)
			#junk.write(oname + '\n')
			#continue
		if len(app.getPossiblevendors()) == 0 and not thorough:
			#an alternative here is to simply use the search functionality, this will take a very long time though
			continue
			
		if len(app.getPossiblevendors()) == 0 and thorough:
			data = {};
			opname = clean_string(oname)
			opname = optimize(opname)
			data['search'] = opname
			url = cve_details_url + searchext + urllib.parse.urlencode(data)
			result = requests.get(url, headers=headers)
			if result.status_code != 200:
				print('request failed')
			else:
				soup = BeautifulSoup(result.content.decode(), 'html.parser')
				table = soup.find('table', attrs={'class': 'listtable'})
				#links = soup.find('table', attrs={'class': 'listtable'}).find_all('a')
				if table:
					links = table.find_all('a')
					vulns = []
					for i in range(0, len(links), 3):
						app.addVendor(optimize(links[i+1].string))
						#print('product: ' + links[i].string)
						#print('vendor: ' + links[i+1].string)
					if len(links) > 0:
						#print(app.getProductname())
						#print(app.getVersions())
						app.setProductname(opname)
						new_object_list.append(app)
						output.write(oname + '\tApplication Identified as:\t' + opname + '\n')
						output.write('++++++++++++++++++++\n')
					continue
				junk.write(oname + '\n')
				continue
			
		'''
		if len(app.getPossiblevendors()) == 0 and thorough:
			opname = clean_string(oname)
			opname = optimize(opname)
			app.setProductname(opname)
			new_object_list.append(app) 
			
			url = 'http://cve.circl.lu/api/search/' + opname
			result = requests.head(url)
			#print(result.headers['content-length'])
			#print(result)
			#print(opname)
			if result.status_code == 200 and int(result.headers['content-length']) > 18:
				print(opname)
				app.setProductname(opname)
				new_object_list.append(app)
				output.write(oname + '\tApplication Identified as:\t' + opname + '\n')
				output.write('--------------------\n')
			else:
				junk.write(oname + '\n')
			'''
			
		possvendors = app.getPossiblevendors()
		for vendor in possvendors:
			tmp = json.load(open('../files/' + vendor + '_productlist.txt'))
			products = products + tmp
		oname = app.getName()	
		name_exact = clean_string(oname)
		name_exact = optimize(name_exact)
		name = closest(products, name_exact, possvendors, ratio)
		if name == '':
			name_simple = cleann_string(oname)
			name_simple = optimize(name_simple)
			name = closest(products, name_simple, possvendors, ratio)
			if name == '':
				#name_nobracs = cleannn_string(oname)
				#name_nobracs = optimize(name_nobracs)
				#name = closest(products, name_simple, possvendors)
				#if name == '':
				junk.write(oname + '\n')
			
		if name != '':
			for vendor in possvendors:
				if name in json.load(open('../files/' + vendor + '_productlist.txt')):
					app.addVendor(vendor)
					break
			app.setProductname(name)
			new_object_list.append(app)
			output.write(oname + '\tApplication Identified as:\t' + name + '\n')
			output.write('--------------------\n')
	return new_object_list
	output.close()
	junk.close()
	
def determine_versions(object_list):
	for obj in object_list:
		name = obj.getName()
		versionlist = vversion.findall(name)
		versionliststr = [x.strip('() ') for x in versionlist]
		java_list = java.findall(name)
		for j in java_list:
			vals = j.split()
			versionliststr.append('1.' + vals[0] + '.0')
			versionliststr.append('update_' + vals[2])
			versionliststr.append('update' + vals[2])
		versions = obj.getVersions()
		for v in versions:
			if rpm.search(v):
				list = v.split('-')
				versionliststr.append(list[0])
				try:
					list = v.split('=')
					versionliststr.append(list[1])
				except:
					pass
		obj.setVersions(versionliststr)
	return object_list
		
'''
if len(app.getPossiblevendors()) == 0:
			app.setPossiblevendors(['oracle'])
		
			opname = java_check(oname)
			opname = optimize(opname)
			url = 'http://cve.circl.lu/api/search/' + opname
			result = requests.get(url)
			if result.status_code == 200:
				app.setProductname(opname)
				new_object_list.append(app)
				output.write(oname + '\tApplication Identified as:\t' + opname + '\n')
				output.write('--------------------\n')
			else:
			'''
	
	
	
	
	
	
	