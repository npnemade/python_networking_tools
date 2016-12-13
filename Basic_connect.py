from jnpr.junos import Device
from getpass import getpass
import sys
import sqlite3

username = raw_input("Enter username: ")
password = getpass("Enter password: ")
filename = raw_input("Enter the name of the file with  list of devices:")

try:
	f = open(filename,'r')
except Exception as err:
	print(err)
	sys.exit(1)

conn = sqlite3.connect('Devices.db')
c = conn.cursor()
c.executescript('DROP TABLE IF EXISTS Details')
c.execute('''CREATE TABLE Details (hostname text, serial text, version text, model text, uptime text)''')

for line in f:
	contents = line.split()
	hostname = contents[0]

	dev = Device(host=hostname, user=username, passwd=password)
	print("\n ==================================================")
	print("\n Connecting to " +hostname + ".......")

	try:
		dev.open()
	except Exception as err:
		print (err)
		sys.exit(1)

	dev_facts = dev.facts
	
	for i in dev_facts:
		print(str(i) + "\t"+ str(dev_facts[i]))
	
	c.execute("INSERT INTO Details VALUES (?,?,?,?,?)",((str(dev_facts['fqdn'])),(str(dev_facts['serialnumber'])),(str(dev_facts['version'])),(str(dev_facts['model'])),(str(dev_facts['RE0']['up_time']))))
	dev.close()
	conn.commit()

conn.close()

	


