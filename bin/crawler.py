import re, json, difflib, requests, datetime
import urllib.request

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}	

'''
<name>-<version>-<release>.src.rpm for source packages, or
<name>-<version>-<release>.<architecture>.rpm for binaries.
all(x in two for x in one)
'''
#Returns true if this is a valid vulnerability, otherwise false. handles one uri at a time
def handle_oval(url):
	#if deprecated return False
	pass

def write_html(applications):
	html = '''
		!doctype html><html><head><title>Results</title><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
		integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"></head><body><h3 class="text-center">Summary of Findings</h3><h4
		class="text-center">Brought to you by CeeVee</h4><table class="table"><thead class="inverse"><tr><th>Vendor</th><th>Product</th><th>Servers</th><th>Versions</th></tr></thead><tbody>'
		'''
	for app in applications:
		pass
		
		
def check_vulnerabilities(app_list):
	vuln_list = []

	output = open('../loot.html', 'w')
	html = '<!doctype html><html><head><title>Results</title><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"></head><body><h3 class="text-center">Summary of Findings</h3><h4 class="text-center">Brought to you by CeeVee</h4><table class="table"><thead class="inverse"><tr><th>Vendor</th><th>Product</th><th>Servers</th><th>Versions</th></tr></thead><tbody>'
	crit = 0
	high = 0
	med = 0
	low = 0
	
	for app in app_list:
		if app.getProductName() == '':
			continue
		try:
			vulns = json.load(open('../files/' + app.getProductName() + '_cve.txt'))
			versions = app.getVersions()
			name = app.getProductName()
			vendor = app.getVendor()
			tmp = '<tr><td>' + vendor + '</td><td>' + name + '</td><td>'
			for each in app.getServers():
				tmp = tmp + each + ' '
			tmp = tmp + '</td><td>'
			for ver in app.getVersions():
				tmp = tmp + ver + ' '
			tmp = tmp + '</td></tr>'
			for vuln in vulns:
				configs = vuln['vulnerable_configuration_cpe_2_2']
				for config in configs:
					list = config.split(':')
					vulnvers = list[4:]
					#package
					if len(vulnvers) == 0:
						continue
					elif set(vulnvers).issubset(versions) and list[2] == vendor and list[3] == name and list[1] == '/a': #uncomment this if you only care about applications
						html = html + tmp + '<tr><td>'
						tmp = ''
						cvs = vuln['cvss']
						if float(cvs) > 7.5:
							style = 'red'
							crit = crit + 1
						elif float(cvs) > 5:
							style = 'orange'
							high = high + 1
						elif float(cvs) > 2.5:
							style = 'yellow'
							med = med + 1
						else:
							style = 'green'
							low = low + 1
						html = html + str(vuln['id']) + '</td><td style="color:' + style + '";>' + str(vuln['cvss']) + '</td><td>' + str(vuln['summary']) + '</td><td>'
						for vul in vulnvers:
							html = html + vul + ' '
						html = html + '</td></tr>'
					else:
						pass
		except Exception as e:
			#skipping missing API 
			pass
	html = html + '</tbody></table></body></html>'
	output.write(html)
	output.close()
	return {'crit': crit, 'high': high, 'med': med, 'low': low}
			
def pull_cve(name, vendor):
	url = 'http://cve.circl.lu/api/search/' + vendor + '/' + name
	result = requests.get(url)
	if result.status_code != 200:
			#There is an error with this API
			output = open('../errors.txt', 'a')
			output.write('[' + str(datetime.datetime.now()) + '] There is no API entry for: ' + url + '\n')
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
			

	
