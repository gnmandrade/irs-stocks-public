#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 20:11:13 2022

Main code of the IRS preparation.
Configurations can be set in the file Config.py
Auxiliar functions are available in the auxilar module.

@author: gnmandrade
"""

# Import libraries
import numpy as np
import pandas as pd

# Import auxiliar functions
import helperFunctions.genAuxFunctions as genAuxF
import helperFunctions.ioAuxFunctions as ioAuxF
import helperFunctions.dfAuxFunctions as dfAuxF

########################
# Import configurations
########################
# Config file
import Config

# Directory and file names
# Working directory
work_dir = Config.work_dir

# Input file name
file_name = Config.file_name
# Output file name
output_file_name = Config.output_file_name

# IRS fiscal year
# Year to declare
irs_yyyy = Config.irs_yyyy

# Columns to use in the final aggregated table
# Columns to keep from the aggregation
columns_to_keep = Config.columns_to_keep
columns_to_sum = Config.columns_to_sum


##########
# Input data
##########

# Read file as DF
transactions_all_history = ioAuxF.excel_to_pd_df(file_name)


##########
# Prepare data
##########

# Add auxiliar columns
# Date column in datetime format
transactions_all_history['date'] = np.vectorize(genAuxF.get_datetime)(transactions_all_history['Date'], transactions_all_history['Hour'])

# Extract year and month
transactions_all_history['year'] = transactions_all_history['date'].dt.year
transactions_all_history['month'] = transactions_all_history['date'].dt.month

# Extract transaction type
transactions_all_history['type'] = np.vectorize(genAuxF.get_type_operation)(transactions_all_history['Quantity'])

# Cast column types
cols_to_cast = {'Value':'float', 'Value_Local':'float', 'Transaction_Fee':'float', 'Quantity':'int'}
transactions_all_history = dfAuxF.df_cast_col_types(transactions_all_history, cols_to_cast)


##########
# Initial Logic
##########
transaction_types = dfAuxF.get_set_from_column_df(transactions_all_history, 'type')
product_types = dfAuxF.get_set_from_column_df(transactions_all_history, 'Product')

# Create one line for each product
reps = list(abs(transactions_all_history['Quantity']))
transactions_all_history_all_stocks = transactions_all_history.loc[np.repeat(transactions_all_history.index.values,reps),:].reset_index(drop = False)
transactions_all_history_all_stocks.rename(columns = {'index':'transaction_index'}, inplace = True)

# Rescale values for each product
cols_to_rescale = ['Value', 'Value_Local', 'Transaction_Fee','Quantity']

for col in cols_to_rescale:
    transactions_all_history_all_stocks.loc[:,col] = np.divide(np.array(transactions_all_history_all_stocks.loc[:,col]), np.abs(transactions_all_history_all_stocks.loc[:,'Quantity']))

##########
# Create column for the stock id index
##########

# Create the column with a default value
transactions_all_history_all_stocks['individual_stock_id'] = 1

# Create Multiindex for transactions_all_history_all_stocks
multi_index_aux_tupples = list(zip(
    np.array(transactions_all_history_all_stocks['type']),
    np.array(transactions_all_history_all_stocks['Product'])
))

multi_index = pd.MultiIndex.from_tuples(tuples = multi_index_aux_tupples, names = ['type','Product'])

transactions_all_history_all_stocks.set_index(multi_index, inplace = True)


# Index should be ordered for improved preformance
# Ordering the index does not preserve the order in the
# dates.
transactions_all_history_all_stocks.sort_index(inplace = True)


# Create index for each unit of each product
for type_trans in multi_index.unique():
    n_stocks = len(transactions_all_history_all_stocks.loc[type_trans,:])
    transactions_all_history_all_stocks.loc[type_trans,:] = transactions_all_history_all_stocks.loc[type_trans,:].sort_values('date', inplace = False) 
    transactions_all_history_all_stocks.loc[type_trans,'individual_stock_id'] = range(1, 1 + n_stocks)

# Cast the individual stock id to an int
transactions_all_history_all_stocks['individual_stock_id'] = np.vectorize(genAuxF.cast_to_int)(transactions_all_history_all_stocks['individual_stock_id'])

##########
# Find which stocks were sold on year yyyy
##########
transactions_all_history_all_stocks.set_index('type',drop = False, inplace = True)
sells_year_yyyy = transactions_all_history_all_stocks.loc['S',:].copy()
sells_year_yyyy.set_index('year', drop = False, inplace = True)
sells_year_yyyy = sells_year_yyyy.loc[irs_yyyy,:]

# Find bought stocks all history
buys_all_history = transactions_all_history_all_stocks.loc['B',:].copy()


# Identify which of the bought stocks were sold
# Join by the individual stock id
joinned_transactions = pd.merge(sells_year_yyyy, buys_all_history, how='inner', on=['Product','individual_stock_id'], suffixes=['_Sells','_Buys'])

#print(transactions_all_history)
##########
# Aggregate data
##########

# Prepare column names
columns_to_sum = genAuxF.add_suffix_to_list('_Sells', columns_to_sum) + genAuxF.add_suffix_to_list('_Buys', columns_to_sum)
columns_to_keep = genAuxF.add_suffix_to_list('_Sells', columns_to_keep) + genAuxF.add_suffix_to_list('_Buys', columns_to_keep)

# Aggregate data to the required granularity
aggfunc = {x: np.sum for x in columns_to_sum}
transactions_groupped = joinned_transactions.pivot_table(values = columns_to_sum, index=columns_to_keep, aggfunc=aggfunc).reset_index()

# Compute column with profits
transactions_groupped['profits'] = transactions_groupped['Value_Buys'] + transactions_groupped['Value_Sells']


##########
# Output aggregated table as excel
##########

# Write outputs in excel
ioAuxF.pd_df_to_excel(output_file_name, transactions_groupped)