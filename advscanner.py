from socket import *
import optparse
from threading import *
from termcolor import colored

# thread to look up
# https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
# https://stackoverflow.com/questions/14167850/socket-programming-in-python-doubts/14168176#14168176

# This function actually performs the scanning part
def Scanner(tgtHost,tgtport):
	try:
		sock=socket(AF_INET,SOCK_STREAM)
		sock.connect((tgtHost,tgtport))
		banner=sock.recv(1024)
		banner = banner.decode('utf-8')
		print(colored('[+] %d/TCP is open'%tgtport,'green'), 
			'\n', 
			colored('[*] '+tgtHost+': '+ str(banner), 'yellow'
		))

	except:
		print(colored('[-] %d/TCP is closed'%tgtport,'red'))

	finally:
		sock.close()

# This is for resolving if the user specifies the host as a name
#and not as a ip, it also prints out
#the name of the website bound to that ip address.
def portScan(tgtHost,tgtPorts):
	try:
		tgtIp=gethostbyname(tgtHost)
	
	except:
		print('[-] Cannot resolve hostname for: '+tgtHost)

	try:
		tgtName=gethostbyaddr(tgtIp)
		print('[+] Hostname: '+tgtName)
	
	except:
		print('[+] Scan results for: '+tgtIp)

	setdefaulttimeout(1)
	for tgtport in tgtPorts:
		t = Thread(target=Scanner, args=(tgtHost,int(tgtport)))
		t.start()



# This is for mainly specifing help,flags and other user related stuff.
# There is not any scanning going on
def main():
	parser = optparse.OptionParser('Usage of program:' + ' -H <target host> -P <target Ports>')
	parser.add_option('-H', dest='tgtHost',type='string',help='Specify target host')
	parser.add_option('-P', dest='tgtPorts',type='string',help='Specify target ports seperated by commas')
	(options,args) = parser.parse_args()
	tgtHost = options.tgtHost
	tgtPorts = str(options.tgtPorts).split(',')
	if(tgtHost == None or tgtPorts[0] == None):
		print(parser.usage)
		exit(0)
	portScan(tgtHost,tgtPorts)


if __name__ == '__main__':
	main()