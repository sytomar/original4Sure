import random
import numpy as np
import decimal
import json
import socket
import sys
import time
import helper

# number of racer.
racer_count = 2
# current lap
current_lap = 0
# last distance calculated
last_distance = None
# last position of all the racers
last_racer1_position = None
last_racer2_position = None					
# current lap details
current_lap_detail = None
# current lap count
current_lap_count = 0
# all the lap information								
laps_details = helper.get_lap_info(racer_count) 

def getLap(current_lap):	
	result = None
	if (1 == laps_details[current_lap]['status']):
		result = {}
		result['m1'] = random.randint(-10,10)
		result['m2'] = random.randint(-10,10)
		result['c1'] = random.randint(-10,10)
		result['c2'] = random.randint(-10,10)
		result['flag'] = 0
		if result['m1'] == 0 and result['m2'] == 0 or result['m1'] == result['m2']:
			return getLap(current_lap)
		else:
			laps_details[current_lap]['Lap'] = "[("+str(result['m1'])+","+str(result['c1'])+"), ("+str(result['m2'])+","+str(result['c2'])+")]"
			return json.dumps(result)
	else: 
		return result

host = "127.0.0.1"
# Reserve a port for the racer.
port_racer1 = 12341
port_racer2 = 12342

socket_conn_racer1 = socket.socket()
socket_conn_racer2 = socket.socket() 
try:
	socket_conn_racer1.connect((host, port_racer1))
	socket_conn_racer2.connect((host, port_racer2))
except socket.error as msg:
	print 'Socket connetion failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print 'Socket connected.'

while True:
	if 10 == current_lap:
		socket_conn_racer1.sendall("0")
		socket_conn_racer2.sendall("0")
		break
	else:
		if last_distance is None:
			current_lap_detail = getLap(current_lap)
			if current_lap_detail is not None:
				try:
					laps_details[current_lap]['LapStart'] = time.time()
					# Send data
					print >>sys.stderr, 'sending "%s"' % current_lap_detail
					socket_conn_racer1.sendall(current_lap_detail)
					socket_conn_racer2.sendall(current_lap_detail)
					# Look for the response
					while True:
						data_r1 = socket_conn_racer1.recv(1024)
						data_r2 = socket_conn_racer2.recv(1024)
						print >>sys.stderr, 'received '+data_r1+" | "+data_r2
						last_racer1_position = json.loads(data_r1)
						last_racer2_position = json.loads(data_r2)
						last_distance = int(last_racer1_position['y']) - int(last_racer2_position['y'])
						if last_distance < 0:
							last_distance = last_distance * (-1)
						break
				finally:
					print >>sys.stderr
					# socket_conn_racer1.close()
					# socket_conn_racer2.close()
			else:
				print "No lap data found."
		else:
			current_lap_count = current_lap_count + 1
			if last_distance < 10:
				lap_data_temp = json.loads(current_lap_detail)
				last_racer1_position['flag'] = 1
				last_racer1_position['m'] = lap_data_temp['m1']
				last_racer1_position['c'] = lap_data_temp['c1']

				last_racer2_position['flag'] = 1
				last_racer2_position['m'] = lap_data_temp['m2']
				last_racer2_position['c'] = lap_data_temp['c2']
				try:
					# Send data
					print >>sys.stderr, 'sending last_points_racer1, last_points_racer2'
					socket_conn_racer1.sendall(json.dumps(last_racer1_position))
					socket_conn_racer2.sendall(json.dumps(last_racer2_position))
					# Look for the response
					while True:
						data_r1 = socket_conn_racer1.recv(1024)
						laps_details[current_lap]['AverageLatencyR1'] = time.time() - laps_details[current_lap]['LapStart']
						data_r2 = socket_conn_racer2.recv(1024)
						laps_details[current_lap]['AverageLatencyR2'] = time.time() - laps_details[current_lap]['LapStart']
						print >>sys.stderr, 'received '+data_r1+" | "+data_r2
						last_racer1_position = json.loads(data_r1)
						last_racer2_position = json.loads(data_r2)
						last_distance = int(last_racer1_position['y']) - int(last_racer2_position['y'])
						if last_distance < 0:
							last_distance = last_distance * (-1)
						break
				finally:
					print >>sys.stderr
			else:
				laps_details[current_lap]['LapEnd'] = time.time()
				laps_details[current_lap]['TimeToCompletion'] = round((laps_details[current_lap]['LapEnd'] - laps_details[current_lap]['LapStart']), 5)
				laps_details[current_lap]['AverageLatencyR1'] = round((laps_details[current_lap]['AverageLatencyR1']/current_lap_count), 5)
				laps_details[current_lap]['AverageLatencyR2'] = round((laps_details[current_lap]['AverageLatencyR2']/current_lap_count), 5)
				laps_details[current_lap]['status'] = 2
				current_lap = current_lap + 1
				laps_details[current_lap]['status'] = 1
				last_distance = None
				last_racer1_position = None
				last_racer2_position = None
				current_lap_detail = None
				current_lap_count = 0
				continue

# Open a file
fo = open("racer.csv", "wb")
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




