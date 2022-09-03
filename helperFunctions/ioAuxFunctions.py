#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 16:17:01 2022

Auxiliar functions to import and export data

@author: gnmandrade
"""

# Import Libraries
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

###################################
###################################
### Input / Output
###################################
###################################

####
# Import Excel File to Python Dictionary
####
# Function that imports an Excel file and stores each sheet as
# an item in a Python Dictionary.
# Each item is a Pandas DataFrame and the associated key is
# the name of the corresponding sheet in the original Excel.

def excel_to_dict(excel_path):
    try:
        excel_object = pd.ExcelFile(excel_path)
        list_of_sheets = excel_object.sheet_names
        excel_dict = {x: excel_object.parse(x) for x in list_of_sheets}
        
        print("Imported excel file:")
        print(excel_path)
        
        return excel_dict

    except:
        error_str = "ERROR!!! - Failled to import " + excel_path
        raise(Exception(error_str))
        return error_str

####
# Import Excel File to Pandas Dataframe
####
# This function uses the excel_to_dict function to import an
# Excel file. It converts the first sheet of the file to a
# Pandas DataFrame.

def excel_to_pd_df(excel_path):
    # Import Excel as Python Dictionary
    excel_dict = excel_to_dict(excel_path)
    
    # Get list of sheets
    sheet_names = list(excel_dict.keys())
    
    # Get the first sheet as a Pandas DataFrame
    excel_df = excel_dict[sheet_names[0]]
    
    return excel_df
    

####
# Export Python Dictionary of Pandas dataframes to Excel
####
# This function gets a Python Dictionary containing Pandas
# DataFrames and stores it as an Excel File with the
# sheet names' given by the dictionary keys.

def dict_to_excel(excel_path, dict_pandas):
    try:
        with pd.ExcelWriter(excel_path, engine = 'openpyxl') as writer:
            for sheet in dict_pandas:
                dict_pandas[sheet].to_excel(writer, sheet_name = sheet, index = False)
        
        
        output_str = "Exported dictionary to Excel file:\n" + excel_path
        print(output_str)
        return output_str
    except:
        error_str = "ERROR!!! - Failled to export " + excel_path
        raise(Exception(error_str))
        return error_str

####
# Export Pandas dataframes to Excel
####
# This function uses the dict_to_excel function to export
# a Pandas DF to an Excel File.
# The sheet name is given by the file name in the path provided.

def pd_df_to_excel(excel_path, df):
    # Get the sheet name from the file path
    try:
        sheet_name = excel_path.split('/')[-1]
    except:
        sheet_name = excel_path.split('\\')[-1]
    
        # Extract sheet name
    sheet_name = sheet_name.split('.')[0]
    
    # Create dictionary with the dataframe
    output_dict = {sheet_name: df}
    
    dict_to_excel(excel_path, output_dict)    