#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 16:46:38 2022

Auxiliar functions to manipulate Pandas Dataframes

@author: gnmandrade
"""

# Import Libraries
import numpy as np

# Costumized Libraries
import helperFunctions.genAuxFunctions as genAuxF

###################################
###################################
### Dataframe Manipulation
###################################
###################################

####
# Function to cast columns to types
#### 
# Makes use of the generic auxiliar functions to cast.
# Receives a list of columns or a dictionary with the final
# column types.
# If the input is a list, the cast_type needs to be defined
# and all columns are converted to that same type.
# Alternatively, a dictionary may be provided and a specific
# type assigned to each column.

def df_cast_col_types(df, casting_iterable, cast_type = ''):
    # Copy the input dataframe
    df_copy = df.copy()
    # Test if cast type was provided
    if cast_type == '':
        # If the cast type was not provided, the casting
        # cannot be made
        if type(casting_iterable) == list:
            raise(Exception("ERROR!!! List was provided with no cast type!!!"))
        
        # Iterate over the columns
        for column_name in casting_iterable:
            # Get casting function
            casting_function = genAuxF.get_cast_function(casting_iterable[column_name])
            
            # Apply casting_function to the column
            df_copy[column_name] = np.vectorize(casting_function)(df_copy[column_name])
        
    else:
        # Get casting function
        casting_function = genAuxF.get_cast_function(cast_type)
        
        # Iterate over the columns
        for column_name in casting_iterable:
            # Apply casting_function to the column
            df_copy[column_name] = np.vectorize(casting_function)(df_copy[column_name])
    
    return df_copy


####
# Function to get a set from a df column's values
####

def get_set_from_column_df(df, column_name):
    output_set = set(df[column_name])
    
    # Prevent the output from being a string
    # This happens when there is only 1 element
    if type(output_set) == str:
        output_set = {output_set}
    
    return output_set