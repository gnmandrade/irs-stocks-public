#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 16:44:19 2022

Auxiliar functions file for the IRS compilation code.

@author: gnmandrade
"""

print("Importing auxiliar functions...")

# Import required libraries
import numpy as np
import datetime


###################################
###################################
### Python Objects manipulation
###################################
###################################

###################
## Casting functions
###################

# Cast individual values
def cast_to_int(value):
    return int(value)

def cast_to_float(value):
    # These commented lines are required for the
    # original Degiro report format, where we have
    # '.' marking the thousands and ',' as a
    # decimal place
    
    #value = str(value)
    #value = value.replace('.','')
    #value = value.replace(',','.')
    return float(value)   

# Decide cast function
# Returns a pointer to the desired cast function
def get_cast_function(final_type):
    if final_type == 'int':
        cast_function = cast_to_int
    elif final_type == 'float':
        cast_function = cast_to_float
    else:
        raise(Exception("ERROR!!! Cast type not supported!!!"))
    
    return cast_function


###################
## Date functions
###################

# Function to get datetime from year and hour
def get_datetime(date, hour):
    date_str = date + ' ' + hour
    return datetime.datetime.strptime(date_str,'%d-%m-%Y %H:%M')


###################
## Other functions
###################


def get_type_operation(quantity):
    quantity = int(quantity)
    direction = quantity / np.abs(quantity)
    if direction < 0:
        return 'S'
    elif direction > 0:
        return 'B'


def add_suffix_to_list(string, list_elements):
    output = [x + string for x in list_elements]
    return output


print("Auxiliar functions imported!!!")