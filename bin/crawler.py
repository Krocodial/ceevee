

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}	

def check_vulnerabilities(app_list):
	for app in app_list:
		vulns = json.load(open('../files/' + app.getProductName() + 'cve'))
		versions = app.getVersions()
		for vuln in vulns:
			configs = vuln['vulnerable_configuration_cpe_2_2']
			for config in configs:
				list = config.split(':')
				if len(list) > 6:
					if list[5] in versions and list[6] in versions:
						print('vulnerable')
				else:
					if list[5] in versions:
						print('vulnerable')
				#parse and look for versions numbers
	
def pull_cves(names):
	for name, vendor in names.keys():
		output = open('../files/' + name + '_cve', 'w')
		url = 'http://cve.circl.lu/api/search/' + vendor + '/' + name
		result = requests.get(url)
		if result.status_code != 200:
			print('There is something wrong with the API')
			exit()
		else:
			try:
				jseen = json.loads(result.content.decode('utf-8'))
				json.dump(jseen, output)
				output.close()
			except Exception as e:
				print(e)
				exit()