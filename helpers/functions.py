#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Classes and functions for calculate accuracy

Read files with forecasted and observed files with indices
Calculate statistics to measure errors and accuracy

"""

import pandas as pd
from datetime import timedelta

class Files:

	"""Works with files
	Read/write files
	"""
	
	def read_obs(self):
		"""Read observed files
		Read NOAA's observed indices in TXT fixed columns file
		"""
		col_specification = [(0,4), (4,8), (9,16), (17,24), (25,32), (33,40), (41,48), (49,56), (57,64), (65,72)]
		dataset = pd.read_fwf('data/sstoi.indices', colspecs=col_specification)
		dataset.columns = ['year', 'month', 'nino12', 'anom12', 'nino3', 'anom3', 'nino4', 'anom4', 'nino34', 'anom34']
		return(dataset)
	
	def forecast_list(self, forec_start):
		"""List forecast files
		List all CSV files in forecast directory
		"""
		import glob
		paths = sorted(glob.glob('data/forecast/*.csv'))
		files = []
		for path in paths:
			# Extract name file withou path
			filename = path.split('/')[-1]
			# Restrict by date
			yearmonth = filename.split('_')[3]
			if int(yearmonth) >= forec_start:
				files.append(filename)
		return(files)
	
	def start_df(self, n_forec, files_forec):
		"""Initialize dataframe
		Create dataframe with 'n_forec' columns and
		define all first date of each forecast run on column 0
		(based on forecast filename)
		"""
		# Create DataFrame
		col_names = range(0,n_forec+1)
		df = pd.DataFrame(columns = col_names)
		# Define first column by name of files
		first_column = []
		for filename in files_forec:
			# Extract date from first forecasted month
			yearmonth = filename.split('_')[3]
			first_column.append(yearmonth)
		# Insert first column with 1st run date from each file
		df[0] = first_column
		return(df)
	
	def read_forecast_row(self, filename, var_for):
		"""Read forecast file row
		Read CSV file with one forecast run into dataframe
		Select variable of interest (row)
		"""
		# Read CSV file
		data = pd.read_csv('data/forecast/%s' %filename)
		# Select var row and n forecast column
		values = data[data['INDEX'] == var_for]
		values = values.drop(columns=['INDEX']).values[0]
		return(values)
		
	def forec_date_row(self, filename):
		"""Get 1st forecast date
		Extract YEARMONTH from string filename
		"""
		# Bash (for older files): rename 's/-/_/g' *
		yearmonth_start = filename.split('_')[3]
		return(yearmonth_start)

	def forec_date(self, yearmonth_start, n):
		"""Calculate forecast date
		Using first forecast date on file name,
		calculate forecast date using column number
		"""
		from datetime import datetime
		from datetime import date
		from dateutil.relativedelta import relativedelta
		# Add month by n
		dt_start = datetime.strptime(yearmonth_start, '%Y%m')
		yearmonth = dt_start + relativedelta(months=+n-1)
		year = int(yearmonth.strftime("%Y"))
		month = int(yearmonth.strftime("%m"))
		return(year, month)

	def select_obs(self, data, var_obs, year, month):
		"""Select observed value
		Try to get observed value from year/month or return None
		"""
		#print(year, month)
		try:
			value = float(data[(data['year'] == year)
			 & (data['month'] == month)][var_obs].reset_index(drop=True))
		except:
			value = None
		return(value)


class Statistics:

	"""Works with statistics
	Calculate metrics to avaliate forecast
	"""
		
	def mape_ind(self, forec_value, obs_value):
		"""Calculate MAPE and accuracy
		Calculate MAPE element for observed/forecast values;
		then, calculate accuracy for this element
		"""
		# Just for doesn't divide by zero
		if obs_value == 0:
			obs_value = 0.01
		# Calculate MAPE and accuracy
		try:
			mape = abs((obs_value - forec_value)/obs_value)*100
			accuracy = int(round(100 - mape))
		except:
			accuracy = None
		#print(obs_value,forec_value)
		return(accuracy)
