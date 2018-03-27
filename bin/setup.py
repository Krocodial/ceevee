import urllib.request
import requests
import json

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
			output = open('../files/' + vendor + '.txt', 'w')
			json.dump(products, output)
			output.close()
		except Exception as e:
			print(e)
			exit()