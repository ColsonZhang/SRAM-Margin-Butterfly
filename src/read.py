# ======================================================================
# filename: read.py
# author: ZhangShen
# time: 2021.01.08
# purpose: deal with the csv files
# ======================================================================
import numpy as np
# import csv

# ======================================================================
# Function name: Read_CSV
# Usage: read data from the CSV file
# Input: the input file name
# Return: the data read
# ======================================================================
def Read_CSV(filename):
    with open(filename,encoding = 'utf-8') as f:
        data = np.loadtxt(f,delimiter = ",", skiprows = 1)
    return data


# ======================================================================
# Function name: Data_Filter
# Usage:  When doing the parameter scaning, multi sets of data will be
#         generated. So the function is used to divide the sets of data.
# Input:  the sets of data to be divided
# Return: the list of data and the number of sets
# ======================================================================
def Data_Filter(data):
    x = []
    y = []

    num_row = len(data)
    num_column = len(data[0])
    for i in range(int(num_column/2)):
        index_x = i*2
        index_y = i*2 + 1
        term_x = [j[index_x] for j in data]
        term_y = [j[index_y] for j in data]
        x.append(term_x)
        y.append(term_y)
    return x,y,int(num_column/2)