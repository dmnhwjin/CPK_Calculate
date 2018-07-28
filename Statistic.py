#!/usr/bin python
""""This module will Load Data from Csv file and calcate GR&R or CPK file"""

__author__ = 'hwjin'
__version__ = '1.0.0'


import sys
import csv
import logging
import numpy as np


logger = logging.getLogger(__name__)
fh = logging.FileHandler('CPK.log')
logger.addHandler(fh)


def load_csv():
	""""Load data from CSV file"""
	path = ''
	data = []
	if len(sys.argv)<2:
		path = input('Please enter path of raw data:')
	else:
		path = sys.argv[-1]
	if path == '':
		raise Exception("Empty input ")
	logger.info(path)
	with open(path, 'r') as csv_file:
		data_reader = csv.reader(csv_file,
				                   delimiter=',',
				                   quotechar='|')
		buf_dat = []
		for row in data_reader:
			buf_dat.append(row)
		for i, row in enumerate(buf_dat):
			if i==1:
				data.append(row[15:])
			if i==2:
				data.append(row[15:])
			if i==3:
				data.append(row[15:])
			if i>5:
				data.append(row[15:])

	return data


def cal_cpk(x=[]):
	"""Calcuate CPK data"""
	pure_data = np.array(x[3:], dtype=float)
	title = x[0]
	ulimit = x[1].strip().replace('"','')
	llimit =x[2].strip().replace('"','')
	std_v = np.std(pure_data, ddof=1)
	avg_v = np.average(pure_data)
	tol_v = float(ulimit)-float(llimit)
	cp = tol_v/(std_v*6)
	cpu= (float(ulimit)-avg_v)/(std_v*3)
	cpl =(avg_v-float(llimit))/(std_v*3)
	cpk = cpu if cpu > cpl else cpl
	return  (title, std_v, avg_v, cp, cpk)


def process_data(data = []):
	"""Process data and convert to List object"""
	cpk_result = list()
	if len(data) == 0:
		raise Exception('process_data', 'empty data dictionary')
	for index_of_col in range(1, len(data[-1])):
		data_row = list()
		for i, row in enumerate(data):
			if i<5:
				data_row.append(row[index_of_col])
			else:
				data_row.append(float(row[index_of_col]))
		logger.debug(data_row)
		row_cpk = cal_cpk(data_row)
		cpk_result.append(row_cpk)
	return cpk_result


def Write_to_file(x):
	"""Write CPK data to File"""
	with open('cpk_result.csv','w') as f:
		f.write('Title, stdev, average, cp, cpk\n')
		for row in x:
			f.write('{},{},{},{},{}\n'.format(row[0],row[1],row[2], row[3], row[4]))


if __name__ == '__main__':
	raw_data = load_csv()
	result = process_data(raw_data)
	Write_to_file(result)

