import re, json, difflib, requests
import urllib.request

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}	

def check_vulnerabilities(app_list):
	output = open('../loot.txt', 'w')
	html = '''
	<!doctype html><html><head><title>Results</title></head><body><table><thead><tr><th>Servers</th><th>name</th><th>actual name</th><th>cve</th><th>cvss</th><th>versions affected</th><th>our 
	versions</th></tr></thead><tbody>
	'''
	for app in app_list:
		if app.getProductName() == '':
			continue
		try:
			vulns = json.load(open('../files/' + app.getProductName() + '_cve.txt'))
			versions = app.getVersions()
			name = app.getProductName()
			vendor = app.getVendor()
			for vuln in vulns:
				configs = vuln['vulnerable_configuration_cpe_2_2']
				for config in configs:
					list = config.split(':')
					vulnvers = list[4:]
					if vulnvers in versions and list[2] == vendor and list[3] == name:# and list[1] == '/a': uncomment this if you only care about applications
						output.write('++++++++++\n')
						for each in app.getServers():
							output.write(each + ' ')
						output.write('\n' + app.getName() + '\n')
						output.write(app.getProductName() + '\n')
						output.write(vuln['id'] + '\n' + vuln['cvss'] + '\n')
						for ver in vulnvers:
							output.write(ver + ' ')
						output.write('\n')
						for i in app.getVersions():
							output.write(i + ' ')
						output.write('\n')
					else:
						pass
		except Exception as e:
			print(e)
	output.close()
			
def pull_cve(name, vendor):
	url = 'http://cve.circl.lu/api/search/' + vendor + '/' + name
	result = requests.get(url)
	if result.status_code != 200:
			#There is an error with this API
			output = open('../errors.txt', 'a')
			output.write('There is no API entry for: ' + url + '\n')
			output.close()
			
	else:
		try:
			raw = json.loads(result.content.decode('utf-8'))
			#print('writing ../files/' + name + '_cve')
			output = open('../files/' + name + '_cve.txt', 'w')
			json.dump(raw, output)
			output.close()
		except exception as e:
			print(e)
	
def pull_cves(associations):
	for name, vendor in associations.items():
		pull_cve(name, vendor)
			

	
