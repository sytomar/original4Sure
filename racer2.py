import random
import numpy as np
import decimal
from time import sleep
import socket
import json
import sys
import helper

host = "127.0.0.1"
# Reserve a port for your service.
port = 12342

# Create a socket object
socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
print >>sys.stderr, 'starting up on '+str(host)+' port '+str(port)

#Bind socket to local host and port
try:
	socket_conn.bind((host, port))
except socket.error as msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print 'Socket bind complete'

#Start listening on socket
socket_conn.listen(10)
print 'Socket now listening on port: '+str(port)

while True:
	# Wait for a connection
	print >>sys.stderr, 'waiting for a connection'
	connection, client_address = socket_conn.accept()
	try:
		print >>sys.stderr, 'connection from', client_address
		print >>sys.stderr, 'R2'
		while True:
			data = connection.recv(1024)
			if len(data):
				if data == "0":
					sys.exit()
				print >>sys.stderr
				print >>sys.stderr, 'received "%s"' % data
				data_received = json.loads(data)
				if 0 == data_received['flag']:
					point = helper.get_intersection_point(data_received['m1'], data_received['m2'], data_received['c1'],data_received['c2'])
					if len(point):
						print >>sys.stderr, 'sending "%s"' % point
						connection.send(point)
					else:
						print >>sys.stderr, 'no more data from', client_address
						break
				else:
					point = helper.get_next_point(data_received['x'], data_received['m'], data_received['c'])
					if len(point):
						print >>sys.stderr, 'sending "%s"' % point
						connection.send(point)
					else:
						print >>sys.stderr, 'no more data from', client_address
						break
			else:
				break
	finally:
		# Clean up the connection
		connection.close()




	
	


