from application import application
from setup import *
from identify import *
from crawler import *

application_list = {}


print('Starting')
print('Processing the supplied csv file, depending on the size this can take a while..')
app_list = parse_csv('../files/software_master.csv')#'../files/software_master.csv')

print('\nUpdating vendorlist')
pull_vendors()

print('Identifying product vendors')
vendorlist = find_vendors(application_list)#application_list)

print('Pulling vendor product lists. This may take some time...')
for vendor in vendorlist:
	pull_products(vendor)

print('Identifying products')
associations = determine_product(application_list)#application_list)
print('Identifying version')
versions = determine_versions(associations)
#This combined with the versions from our csv file should be enough. Time to start integrating
"""
application lists[name] = [vendor]
associations[name] = R_name
versions[name] = [versions..]
obj.update ^^^^
"""
print('Updating objects')
real_names = update(app_list, application_list, associations, versions)

#Debugging
output = open('../info.txt', 'w')
for app in app_list:
	if app.getProductName() != '':
		output.write(app.getName())
		output.write('\t ------>  ')
		output.write(app.getProductName())
		output.write('\n')
		output.write(', '.join(app.getVersions()))
		output.write('\n------------------------\n')
output.close()

print('Pulling cves. This can also take some time...')
pull_cves(real_names)

print('Crawling for vulnerabilities')
vulnerabilities = check_vulnerabilities(app_list)#associations, versions)

print('cleaning up')
clean()

print('-------finished-------')
print('Critical:\t' + str(vulnerabilities['crit']))
print('High:\t\t' + str(vulnerabilities['high']))
print('Medium:\t\t' + str(vulnerabilities['med']))
print('Low:\t\t' + str(vulnerabilities['low']))
print('View Identified vulnerabilities in ~/loot.txt')
print("You may also want to check ~/no_id.txt where I've put programs I couldn't identify")
print('Errors such as missing API entries are logged in ~/errors.txt')
print('Come back anytime!')