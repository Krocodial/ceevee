import csv, json, re, datetime, os, requests, sys
from application import application
from multiprocessing import Queue

addriver = re.compile('^XA650.', re.DOTALL)

def parse(name):
	list = []
	counter = 1
	#output = open('../error.txt', 'a')
	try:
		input = csv.reader(open(name))
		for line in input:
			break
		row_count = sum(1 for i in csv.reader(open(name)))
		itera = int(row_count/100)
		for line in input:
			if not counter % itera:
				print('\rProcessed: ' + str(counter//itera) + '%', end='')
				
			counter = counter + 1
			flag = 1
			
			if len(line) < 3:
				print('\rProcessed: 100%', end='')
				break
				
			server = line[0]
			name = line[1]
			version = line[2]

			if addriver.match(name): #useless drivers
					continue
			
			for obj in list:
				if obj.getName() == name and version in obj.getVersions():#set(version).issubset(obj.getVersions()):# not in obj.getVersions():
					obj.addServer(server)
					flag = 0
					break
			if flag == 1:
				tmp = application(name, version, server)
				list.append(tmp)
		return list
		
	except Exception as e:
		#print(os.getcwd())
		output = open('../errors.txt', 'a')
		output.write('[' + str(datetime.datetime.now()) + '] ' + str(e) + '\n')
		output.close()
		print('View errors in ~/errors.txt, exiting....')
		sys.exit()
		
		
def pull_vendors():
	output = open('../files/vendors.txt', 'w')
	
	result = requests.get('https://cve.circl.lu/api/browse')
	if result.status_code != 200:
		output = open('../errors.txt', 'a')
		output.write('[' + str(datetime.datetime.now()) + '] Failed to pull master vendor list: ' + url + '\n')
		output.close()
		print('There is something wrong with the API, check ~/errors.txt for more information')
		sys.exit()
	else:
		try:
			dic = json.loads(result.content.decode('utf-8'))
			vendors = dic['vendor']
			json.dump(vendors, output)
			output.close()
		except Exception as e:
			output = open('../errors.txt', 'a')
			output.write('[' + str(datetime.datetime.now()) + '] ' + str(e) + '\n')
			output.close()
			print('Failed to parse master vendor list, view more information in ~/errors.txt')
			sys.exit()
		
def find_vendors(object_list):
	vendors = json.load(open('../files/vendors.txt'))
	#pre-fill with 10 most common vendors
	vendorlist = ['microsoft', 'oracle', 'apple', 'ibm', 'google', 'cisco', 'adobe', 'linux', 'mozilla', 'redhat']
	
	for vendor in vendors:
		q = re.compile(vendor, re.IGNORECASE)
		for obj in object_list:
			if q.search(obj.getName()):
				obj.addPossiblevendor(vendor)
				if vendor not in vendorlist:
					vendorlist.append(vendor)
	#vendor_output = open('../files/vendors.txt', 'w')
	#json.dump(vendorlist, vendor_output)
	return vendorlist
	
def pull_products(vendor):
	result = requests.get('https://cve.circl.lu/api/browse/' + vendor)
	if result.status_code != 200:
		result = requests.get('https://cve.circl.lu/api/browse/' + vendor)
		if result.status_code != 200:
			print("I'm having trouble grabbing " + vendor + "'s product list, retrying")
			result = requests.get('https://cve.circl.lu/api/browse/' + vendor)
			if result.status_code != 200:
				print("Couldn't grab " + vendor + "'s product list")
		#sys.exit()
	try:
		raw = json.loads(result.content.decode('utf-8'))
		products = raw['product']
		output = open('../files/' + vendor + '_productlist.txt', 'w')
		json.dump(products, output)
		output.close()
	except Exception as e:
		output = open('../errors.txt', 'a')
		output.write('[' + str(datetime.datetime.now()) + '] ' + str(e) + '\n')
		output.close()
		print('Failed to parse ' + str(vendor) + 's product list, view more information in ~/errors.txt')
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		