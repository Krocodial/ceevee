import re, json, difflib, urllib.request, requests
from application import application

"""
This is supposedly a lot faster since it requires C compatibility. 
import Levenshtein
print(Levenshtein.ratio('hellosd', 'sdklf'))
"""

def closest(products, name):
	highest = 0
	value = ''
	for product in products:
		current = difflib.SequenceMatcher(None, name, product).ratio()
		if current > highest:
			value = product
			highest = current
			print(highest)
			print(name + '\t' + value + '\n')
	print('---------------------------------')
	return value
	#return min(products, key=lambda v: len(set(name) ^ set(v)))


	
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'};	
spaces = re.compile(' ')
plus = re.compile('\+')

version = re.compile(r'\s[\S]*[\d]+.', re.DOTALL)
addriver = re.compile('^XA650.', re.DOTALL)
bracs = re.compile('[(].[)]', re.DOTALL)

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
		
	#VERSION NUMBERS
	match = version.search(string)
	if match:
		string = string[:match.start()]
		
	#BRACKETS
	string = bracs.sub('', string)
	
	if len(words) > 1:
		#remove the vendor name?
		pass
	
	return string
		
def optimize(string):
	#optimization rules to find closest match via API
	optimized = plus.sub('%2b', string)
	optimized = spaces.sub('_', optimized)
	optimized = optimized.lower()
	return optimized
	
json_input = json.load(open('json_MList.txt'))
vendorlist = json_input['vendors']

sw_input = open('shortlist.txt')

sw_list = []

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
		"""
		TODO
		remove vendor name before comparing ratio
		disregard low ratio results
		convert '#' to %23
		"""
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
print(software + '---->')
print(vendor_match)
print('++++')

Put all vendor/products in a DB, query from there. 
"""
