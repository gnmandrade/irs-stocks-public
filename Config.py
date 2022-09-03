#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 16:43:18 2022

Configuration file for the IRS compilation code.

@author: gnmandrade
"""

print("Importing configuration file...")

################
# Configurations
################

# Working directory (where the main code is)
work_dir = '//your_path//irs-stocks-public//'

# Input file name
file_name = work_dir + 'Transactions_template.xls'
# Output file name
output_file_name = work_dir + 'Aggregated_file.xls'

# Year to declare
irs_yyyy = '2021'

# Columns to keep from the aggregation
columns_to_keep = ['Stock_Exchange']
columns_to_sum = ['Quantity', 'Value', 'Transaction_Fee']


# Add auxiliar columns
columns_to_keep = columns_to_keep + ['type', 'year', 'month']


print("Configuration file imported...")
