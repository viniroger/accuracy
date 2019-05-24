#!/usr/bin/python
# -*- coding: utf-8 -*-
# Forecast accuracy calculation

import pandas as pd
import sys
sys.path.insert(0,'helpers')
import functions

files = functions.Files()
stats = functions.Statistics()

# Define variable to work
var_obs = 'anom34'
var_for = 'Nino3.4'
forec_start = 200101

# Read observed data
obs_data = files.read_obs()

# List with forecast's filenames (each one is a model run)
files_forec = files.forecast_list(forec_start)

# Number of forecasts by model run
n_forec = 12
# Initialize dataframe to receive monthly accuracies
df = files.start_df(n_forec, files_forec)

# Join 1st date's run (rows) and forecast's numbers (column)
for filename in files_forec:
	# Extract forecast value from var
	forec_row = files.read_forecast_row(filename, var_for)
	# Get 1st forecast date
	yearmonth = files.forec_date_row(filename)
	# Save into dataframe
	df.loc[df[0] == yearmonth, 1:12] = forec_row
# Save dataframe with forecasted values in CSV file
df.to_csv('data/forec_%s.csv' %var_obs, index=False)

# Calculate MAPE for each value on dataframe
column_names = range(1,n_forec+1)
# Loop on rows
for nrow, values in df[column_names].iterrows():
	# Get 1st forec date
	yearmonth = df.iloc[nrow][0]
	# Loop on columns
	for ncol, value in enumerate(values):
		# Calculate forecast date
		year, month = files.forec_date(yearmonth, ncol+1)
		# Get frecasted value
		forec_value = value
		# Get observed value
		obs_value = files.select_obs(obs_data, var_obs, year, month)
		# Replace value by its accuracy
		df.iloc[nrow,ncol+1] = stats.mape_ind(forec_value, obs_value)
	#exit()
# Save dataframe with statistics in CSV file
df.to_csv('data/stats_%s.csv' %var_obs, index=False)

# Calculate median for each column/run
print(df.median())
