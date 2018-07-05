import random
import numpy as np
import decimal
import socket
import json
import time

def get_intersection_point(m1, m2, c1, c2):
	response = {}
	equation_left = np.array([[1, (-1*m1)], [1, (-1*m2)]])
	equation_right = np.array([c1, c2])
	result = np.linalg.solve(equation_left, equation_right)
	response['x'] = round(result[0],2)
	response['y'] = round(result[1],2)
	return json.dumps(response)

def get_next_point(x, m, c):
	time.sleep(0.50)
	next_point = {}
	next_point['x'] = x + 1
	next_point['y'] = round((m*next_point['x'] + c),2)
	return json.dumps(next_point)

def get_distance(points):
	lowest_value = 0
	highest_value = 0
	if len(points):
		lowest_value = int(points[0]['y'])
		highest_value = int(points[0]['y'])
		for point in points:
			if lowest_value > points[point]['y']:
				lowest_value = int(points[point]['y'])
			if highest_value < points[point]['y']:
				highest_value = int(points[point]['y'])
	last_diff = highest_value - lowest_value
	if last_diff < 0:
		last_diff = last_diff * (-1)
	return last_diff

def get_lap_info(racer_count):
	laps_detail = []
	for x in range(0,11):
		lap_detail = {}
		if x == 0:
			lap_detail['LapNumber'] = x+1
			lap_detail['status'] = 1
		else:
			lap_detail['LapNumber'] = x+1
			lap_detail['status'] = 0
		for racer in xrange(racer_count):
			lap_detail['AverageLatencyR'+str(racer+1)] = 0
		lap_detail['Lap'] = ""
		lap_detail['LapStart'] = 0
		lap_detail['LapEnd'] = 0
		lap_detail['TimeToCompletion'] = 0
		laps_detail.append(lap_detail)
	return laps_detail