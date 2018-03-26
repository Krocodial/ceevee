import re, json, difflib, urllib.request, requests

def closest(a, b):
	products = a
	name = b
	return min(products, key=lambda v: len(set(name) ^ set(v)))


	
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'};	
spaces = re.compile(' ')
plus = re.compile('\+')

def optimize(string):
	#optimization rules to find closest match via API
	optimized = plus.sub('%2b', string)
	optimized = spaces.sub('_', optimized)
	optimized = optimized.lower()
	return optimized
	
json_input = json.load(open('json_MList.txt'))
vendorlist = json_input['vendors']

sw_input = open('shortlist.txt')

#check if vendor is in sw?
for line in sw_input:
	vendor_match = []
	software = line[:-1]
	for vendor in vendorlist:
		q = re.compile(r'\b'+vendor+r'\b', re.IGNORECASE)
		if q.search(software):
			vendor_match.append(vendor)
	if len(vendor_match) > 0:
		optimized = optimize(software)
		
		products = []
		for each in vendor_match:
			url = 'http://cve.circl.lu/api/browse/' + each
			result = requests.get(url, headers=headers)
			if result.status_code != 200:
				print('request failed' + url)
			else:
				tmp = json.loads(result.content.decode('utf-8'))
				products = products + tmp['product']
				
		print(software + '\t' + closest(products, optimized))
		
		"""
		print(software + '---->')
		print(vendor_match)
		print('++++')
		"""
"""
Put all vendor/products in a DB, query from there. 
"""
