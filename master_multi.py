import random
import numpy as np
import decimal
import json
import socket
import sys
import time
import helper
import os

# To compute the number of racer.
racer_count = 2
if len(sys.argv) >= 2:
	try:
		if int(sys.argv[1]) > 1:
			racer_count = int(sys.argv[1])
	except Exception as e:
		print e
		sys.exit()

# current lap
current_lap = 0
# last distance calculated
last_distance = None
# last position of all the racers					
last_racer_position = {}
# current lap details
current_lap_detail = None
# current lap count
current_lap_count = 0
# all the lap information								
laps_details = helper.get_lap_info(racer_count) 		

def getLap(current_lap, racer_num):	
	result = None
	if (1 == laps_details[current_lap]['status']) and racer_num > 1:
		result = {}
		lap = "["
		for x in xrange(racer_num):
			result[x] = {
				'm' : random.randint(-10,10),
				'c' : random.randint(-10,10)
			}
			if x != 0:
				lap = lap + ", "
			lap = lap + "("+str(result[x]['m'])+","+str(result[x]['c'])+")"
			result['flag'] = 0
		lap = lap + "]"
		if result[0]['m'] == result[1]['m']:
			return getLap(current_lap, racer_num)
		else:
			laps_details[current_lap]['Lap'] = lap
			return json.dumps(result)
	else: 
		return result

host = "127.0.0.1"
# Reserve a port for your service.
port = 12340

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

halt_status = True
while halt_status:
	# Wait for a connection
	print >>sys.stderr, 'Waiting for a connection:'
	connection, client_address = socket_conn.accept()
	try:
		print >>sys.stderr, 'connection from', client_address
		while True:
			data = connection.recv(1024)
			if len(data) and data == "1":
				while True:
					if 10 == current_lap:
						connection.send("0")
						break
					else:
						if last_distance is None:
							current_lap_detail = getLap(current_lap, racer_count)
							if current_lap_detail is not None:
								try:
									laps_details[current_lap]['LapStart'] = time.time()
									# Send data
									print >>sys.stderr, 'sending "%s"' % current_lap_detail
									connection.send(current_lap_detail)
									while True:
										data = connection.recv(1024)
										print >>sys.stderr, 'received '+data
										for x in range(racer_count):
											last_racer_position[x] = json.loads(data)
											last_distance = 0
										break
								finally:
									print >>sys.stderr
							else:
								print "No lap data found."
						else:
							current_lap_count = current_lap_count + 1
							if last_distance < 10:
								current_lap_detail_temp = json.loads(current_lap_detail)
								for x in range(racer_count):
									last_racer_position[x]['flag'] = 1
									last_racer_position[x]['m'] = current_lap_detail_temp[str(x)]['m']
									last_racer_position[x]['c'] = current_lap_detail_temp[str(x)]['c']
									laps_details[current_lap]['AverageLatencyR'+str(x + 1)] = time.time() - laps_details[current_lap]['LapStart']
									try:
										# Send data
										print >>sys.stderr, 'sending to Racer'+str(x+1)
										connection.send(json.dumps(last_racer_position[x]))
										# Look for the response
										while True:
											data = connection.recv(1024)
											print >>sys.stderr, 'received '+data
											last_racer_position[x] = json.loads(data)
											break
									finally:
										print >>sys.stderr
								last_distance = helper.get_distance(last_racer_position)
							else:
								laps_details[current_lap]['LapEnd'] = time.time()
								laps_details[current_lap]['TimeToCompletion'] = round((laps_details[current_lap]['LapEnd'] - laps_details[current_lap]['LapStart']), 5)
								laps_details[current_lap]['status'] = 2
								for x in xrange(racer_count):
									laps_details[current_lap]['AverageLatencyR'+str(x + 1)] = round((laps_details[current_lap]['AverageLatencyR'+str(x + 1)]/current_lap_count), 5)

								current_lap = current_lap + 1
								laps_details[current_lap]['status'] = 1
								last_distance = None
								last_racer_position = {}
								current_lap_detail = None
								current_lap_count = 0
								continue
			elif len(data) and data == "0":
				halt_status = False
				break
	finally:
		# Clean up the connection
		connection.close()

# Open a file
fo = open("multi_racer.csv", "wb")
fo.write("LapNumber,Lap,LapStart,LapEnd,TimeToCompletion")
for x in xrange(racer_count):
	fo.write(",AverageLatencyR"+str(x+1))
fo.write("\n")
for lap_detail in laps_details:
	if lap_detail['LapNumber'] == 11:
		break
	else:
		fo.write(str(lap_detail['LapNumber'])+",")
		fo.write(str(lap_detail['Lap'])+",")
		fo.write(str(lap_detail['LapStart'])+",")
		fo.write(str(lap_detail['LapEnd'])+",")
		fo.write(str(lap_detail['TimeToCompletion']))
		for x in xrange(racer_count):
			fo.write(","+str(lap_detail['AverageLatencyR'+str(x+1)]))
		fo.write("\n")
fo.close()

