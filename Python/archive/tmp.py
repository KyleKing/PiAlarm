#!/usr/bin/python3

from urllib.request import urlopen
ip = urlopen('http://ipaddr.me/').read()
ip = ip.decode('utf-8')
print (ip)

import socket
name, alias, addresslist = socket.gethostbyaddr(ip)
print (name)
