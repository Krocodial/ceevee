import urllib.request
import requests
import json
import re, os
from application import application

spaces = re.compile(' ')
plus = re.compile('\+')
version = re.compile(r'\s[\S]*[\d]+.', re.DOTALL)
addriver = re.compile('^XA650.', re.DOTALL)
bracs = re.compile('[(].[)]', re.DOTALL)

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

#Pre-parse so we can identify tricky vendors			
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
	sw_input = open('../files/shortlist.txt')

	vendorlist = []
	sw_products = []
	
	for line in sw_input:
		software = line[:-1]
		if addriver.match(software):
			continue
		software = preparse(software)
		sw_products.append(software)
		
		
	for vendor in vendors:
		q = re.compile(r'(\b|^)' + vendor + r'\b', re.IGNORECASE)
		for product in sw_products:
			if q.search(product):
				if product not in application_list:
					application_list[product] = [vendor]
				else:
					application_list[product].append(vendor)
					
				if vendor not in vendorlist:
					vendorlist.append(vendor)
					
	#update vendors.txt, this saves us a lot of runtime
	vendor_output = open('../files/vendors.txt', 'w')
	json.dump(vendorlist, vendor_output)
	
	return vendorlist
	
	
def clean():
	os.remove('../files/*_productlist.txt')
	