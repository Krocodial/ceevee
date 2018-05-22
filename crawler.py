import csv, re, json, os, urllib.request, requests, datetime, sys
from multiprocessing import Queue
from application import vulnerability

q = re.compile('SP\d')
java = re.compile('update \d+', re.IGNORECASE)
rjava = re.compile('update\d+', re.IGNORECASE)
jav = re.compile('java', re.IGNORECASE)
javas = re.compile('update_\d+', re.IGNORECASE)

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}	


def not_in(vuln_app_list, name, versions, servers):
	for app in vuln_app_list:
		if app.getProductname() == name and set(versions).issubset(app.getVersions()) and set(servers).issubset(app.getServers()):
			return False
		elif app.getProductname() == name and set(versions).issubset(app.getVersions()) and not set(servers).issubset(app.getServers()):
			for serv in servers:
				app.addServer(serv)
	return True
		
def vulns_not(vuln_app_list, name, servers, vulnerable_versions):
	for app in vuln_app_list:
		vulnVs = []
		for vuln in app.getVulns():
			vulnVs = vulnVs + vuln.getVuln_versions()
		if app.getProductname() == name and set(vulnerable_versions).issubset(vulnVs) and set(servers).issubset(app.getServers()):
			return False
	return True
		
#def verify(vuln_app_list, vulnvers
		
def check_vulnerabilities(object_list):
	vuln_app_list = []
	vuln_list = []	
	vulnerable_versions = []
	for app in object_list:
		if app.getProductname() == '':
			continue
		r_name = app.getName()
		versions = app.getVersions()
		name = app.getProductname()
		servers = app.getServers()
		for vendor in app.getVendors():
			try:
				vulns = json.load(open('../files/' + vendor + '_' + app.getProductname() + '_cve.txt'))
			except Exception as e:
				output = open('../errors.txt', 'a')
				output.write('[' + str(datetime.datetime.now()) + '] ' + str(e) + '\n')
				output.close()
				continue
			'''
			r_name = app.getName()
			versions = app.getVersions()
			name = app.getProductname()
			vendor = app.getVendor()
			servers = app.getServers()
			'''
			if not_in(vuln_app_list, name, versions, servers):
				if q.search(r_name):
					flag = 1
				elif jav.search(r_name) and java.search(r_name):
					flag = 2
				else:
					flag = 0
				for vuln in vulns:
					configs = vuln['vulnerable_configuration_cpe_2_2']
					for config in configs:
						list = config.split(':')
						vulnvers = list[4:]
						#package
						if len(vulnvers) == 0:
							continue
						elif len(vulnvers) < 2 and flag != 0:
							pass
						elif set(vulnvers).issubset(versions) and list[2] == vendor and list[3] == name and list[1] == '/a':# and list[2] == vendor: #uncomment this if you only care about applications
							if flag == 1:
								if q.search(vulnvers[1]):
									vuln_list.append(vulnerability(vuln['id'], 'https://www.cvedetails.com/cve/' + vuln['id'] + '/', vuln['summary'], vuln['cvss'], vulnvers))
									vulnerable_versions = vulnerable_versions + vulnvers
							elif flag == 2:
								if rjava.search(vulnvers[1]) or javas.search(vulnvers[1]):
									vuln_list.append(vulnerability(vuln['id'], 'https://www.cvedetails.com/cve/' + vuln['id'] + '/', vuln['summary'], vuln['cvss'], vulnvers))
									vulnerable_versions = vulnerable_versions + vulnvers
							else:
								vuln_list.append(vulnerability(vuln['id'], 'https://www.cvedetails.com/cve/' + vuln['id'] + '/', vuln['summary'], vuln['cvss'], vulnvers))
								vulnerable_versions = vulnerable_versions + vulnvers
							break
						else:
							pass
			if vulns_not(vuln_app_list, name, servers, vulnerable_versions):
				app.addVulns(vuln_list)
				vuln_app_list.append(app)
			vuln_list = []
			vulnerable_versions = []
		'''
		except Exception as e:
			#skipping missing API 
			output = open('../errors.txt', 'a')
			output.write('[' + str(datetime.datetime.now()) + '] ' + str(e) + '\n')
			output.close()
		'''
	return vuln_app_list
			
	
def write_out(object_list):
	with open('../loot.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Name Detected', 'Actual Name', 'Versions detected', 'Vulnerable versions', 'CVSS', 'Link to CVE', 'Servers'])
		for app in object_list:
			vulns = app.getVulns()
			for vuln in vulns:
				writer.writerow([app.getProductname(), app.getName(), app.getVersions(), vuln.getVuln_versions(), vuln.getCvss(), '=HYPERLINK("' + vuln.getUrl() + '", "' + vuln.getCve() + '")', app.getServers()])

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
			output = open('../files/' + vendor + '_' + name + '_cve.txt', 'w')
			json.dump(raw, output)
			output.close()
		except exception as e:
			print(e)
	
def pull_cves(object_list):
	names = []
	for obj in object_list:
		name = obj.getProductname()
		for vendor in obj.getVendors():	
			if str(vendor + name) not in names:
				pull_cve(name, vendor)
				names.append(str(vendor+name))
			else:
				pass
				
def clean():
	pattern_cves = re.compile('.cve.txt')
	pattern = re.compile('.productlist.txt')
	for f in os.listdir('../files/'):
		if re.search(pattern, f) or re.search(pattern_cves, f):
			os.remove(os.path.join('../files/', f))