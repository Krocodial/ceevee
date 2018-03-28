from application import application
from setup import *
from identify import *
from crawler import *

application_list = {}


print('Starting')
print('Processing the supplied csv file, depending on the size this can take a while..')
app_list = parse_csv('../files/software_master.csv')

print('Updating vendorlist')
pull_vendors()

print('Identifying product vendors')
vendorlist = find_vendors(application_list)

print('Pulling vendor product lists. This may take some time...')
for vendor in vendorlist:
	pull_products(vendor)

print('Identifying products')
associations = determine_product(application_list)
print('Identifying version')
versions = determine_versions(associations)
#This combined with the versions from our csv file should be enough. Time to start integrating

print('Crawling for vulnerabilities')
vulnerabilities = check_vulnerabilities(associations, versions)

print('cleaning up')
clean()

print('-------finished-------')
print('View Identified vulnerabilities in ~/loot.txt')
print("You may also want to check ~/no_id.txt where I've put programs I couldn't identify")
print('Come back anytime!')