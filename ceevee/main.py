import analysis
import identify
import crawler
import datetime
import sys


file = '../files/software.csv'
ratio = .8
thorough = True


file = '../files/' + input('Enter filename: ')
#if input('Run a complex scan? (y/n) ') == 'y':
#	thorough = True
if input('Change the default match ratio? (y/n) ') == 'y':
	ratio = float(input('Enter a float between 0-1: '))
'''
if len(sys.argv) > 1:
	if sys.argv[1] == 'help':
		print(Welcome to CeeVee\n
Usage: python main.py [options] [file]\n
Options:\n
	-r [0-1] //Enter the ratio used to identify products, lower ratio will result in more false positives.(By default .8 it used)\n
	-t //Thorough search, if the product cannot be identified use general search queries. This can take a long time.\n
File:\n
	Note: if a file is given it should be in the files/ directory and in csv format.\n

		)
		sys.exit()
	for i in range(1, len(sys.argv)):
		try:
			if sys.argv[i] == '-t':
				thorough = True
			if sys.argv[i] == '-r':
				ratio = float(sys.argv[i+1])
			if sys.argv[i].endswith('.csv'):
				file = '../files/' + sys.argv[i]
		except:
			print("'python main.py help' to see a list of possible arguments")
			sys.exit()
'''		
print('['+ str(datetime.datetime.now().time()) +'] Initializing parsing')
object_list = analysis.parse(file)


print('\n['+ str(datetime.datetime.now().time()) +'] Updating vendor list')
analysis.pull_vendors()


print('['+ str(datetime.datetime.now().time()) +'] Identifying vendors')
vendorlist = analysis.find_vendors(object_list)


print('['+ str(datetime.datetime.now().time()) +'] Pulling vendor product lists')
for vendor in vendorlist:
	analysis.pull_products(vendor)

	
print('['+ str(datetime.datetime.now().time()) +'] Identifying products')
object_list = identify.determine_products(object_list, ratio, thorough)


print('['+ str(datetime.datetime.now().time()) +'] Identifying versions')
object_list = identify.determine_versions(object_list)


print('['+ str(datetime.datetime.now().time()) +'] Pulling cves')
crawler.pull_cves(object_list)


print('['+ str(datetime.datetime.now().time()) +'] Crawling for vulnerabilities')
vulnerabilities = crawler.check_vulnerabilities(object_list)


print('['+ str(datetime.datetime.now().time()) +'] Writing out')
crawler.write_out(vulnerabilities)


print('['+ str(datetime.datetime.now().time()) +'] Cleaning up')
crawler.clean()

print('----------finished----------')
print('View Identified vulnerabilities in ~/loot.csv')
print("you may also want to check ~/no_id.txt where I've put applications I couldn't identify")
print("Errors such as missing API entries, or missing vendor entries are all logged in ~/errors.txt")
print('Come back anytime!')