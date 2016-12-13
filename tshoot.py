from jnpr.junos import Device
from getpass import getpass
from lxml import etree

#username = raw_input("Enter username: ")
#password = getpass("Enter password: ")
#deviceName = raw_input("Enter the name of the file with  list of devices:")

def displayIntf( tree ):
	for node in tree:
		if (len(node.getchildren())>0):
			nodeChild = node.getchildren()
			for n in nodeChild:
				displayIntf(n)
		else:
			if ((str(node.tag).lstrip("\n")) == "name"):
				print "==================================================="
				print "NAME :" + "\t" + (str(node.text).lstrip("\n"))
			elif ((str(node.tag).lstrip("\n")) == "admin-status"):			
				print "Admin-Status :" + "\t" + (str(node.text).lstrip("\n"))
			elif ((str(node.tag).lstrip("\n")) == "oper-status"):			
				print "Operational-Status :" + "\t" + (str(node.text).lstrip("\n"))
	return


username = ''
password = ''
deviceName = ''

dev = Device(host=deviceName, user=username, passwd=password)
print("\n ==================================================")
print("\n Connecting to " +deviceName + ".......")

try:
	dev.open()
except Exception as err:
	print (err)
	sys.exit(1)

intfXML = dev.rpc.get_interface_information(terse=True)		# RPC call for show interface terse. Returns an XML structure
#intfXMLString = etree.tostring(intfXML,pretty_print=True)	
#print intfXMLString

displayIntf(intfXML)     									# Psss the XML tree as an argument to displayIntf which recursively cals itself at each node.

dev.close()
