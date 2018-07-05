import random
import numpy as np
import decimal
from time import sleep
import socket
import json
import sys
import helper

connected = 0

host = "127.0.0.1"
# Reserve a port for your service.
port_master = 12340

socket_conn = socket.socket()
try:
	socket_conn.connect((host, port_master))
except socket.error as msg:
	print 'Socket connetion failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print 'Socket connected.'

while True:
	if 0 == connected:
		socket_conn.sendall("1")
		# Look for the response
		while True:
			print >>sys.stderr
			data = socket_conn.recv(1024)
			if data == "0":
				socket_conn.send("0")
				sys.exit()
			print >>sys.stderr, 'received "%s"' % data
			data_received = json.loads(data)
			if 0 == data_received['flag']:
				point = helper.get_intersection_point(data_received['0']['m'], data_received['1']['m'], data_received['0']['c'],data_received['1']['c'])
				if len(point):
					print >>sys.stderr, 'sending to master"%s"' % point
					socket_conn.send(point)
				else:
					print >>sys.stderr, 'no more data'
					break
			else:
				point = helper.get_next_point(data_received['x'], data_received['m'], data_received['c'])
				if len(point):
					print >>sys.stderr, 'sending to master"%s"' % point
					socket_conn.send(point)
				else:
					print >>sys.stderr, 'no more data from'
					break
	else:
		print "already connected"
	break