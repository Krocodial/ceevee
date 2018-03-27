from application import application
from setup import *
from identify import *

application_list = {}

print('Updating vendorlist')
pull_vendors()

print('Identifying product vendors')
vendorlist = find_vendors(application_list)

print('Pulling vendor product lists. This may take some time...')
for vendor in vendorlist:
	pull_products(vendor)

print('Identifying products')
application_list = determine_product(application_list)


	
print('cleaning up')
clean()
print('Come back anytime!')