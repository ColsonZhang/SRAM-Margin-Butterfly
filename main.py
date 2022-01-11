# ======================================================================
# filename: butterfly.py
# author: ZhangShen
# email: colson_z@outlook.com
# time: 2021.01.11
# purpose: the example of the sram_butterfly
# ======================================================================

import sys
import numpy as np
sys.path.append("./src")
from draw import *
from margin import *
from read import *
from butterfly import *
import matplotlib.pyplot as plt



def process(file1,file2,mode):

    the_zeros = 0
    the_start =-1.2
    the_end = 1.2
    the_span = 1.2

    # find the margin
    if (mode == "read") or (mode == "hold") :
        margins,curve_1,curve_2,squares = multi_margin_find(file1, file2, mode=mode, 
                                                    zeros=the_zeros,start=the_start,end=the_end, line_span=the_span,
                                                    auto_zero=True, auto_start=True)
    elif (mode == "write"):
        margins,curve_1,curve_2,squares = multi_margin_find(filename_5, filename_6, mode="write", 
                                                    zeros=the_zeros,start=the_start,end=the_end, line_span=the_span,
                                                    auto_zero=True, auto_start=True,
                                                    search_ratio=0.7)
    else:
        return
    
    number_curves = 5
    the_row = 1
    the_column = 5
    the_titles = ["tt", "ss", "sf", "fs", "ff"]
    # draw the butterfly
    margin_draw(curve_1,curve_2,squares,number=number_curves,titles=the_titles, rows=the_row, columns=the_column)



if __name__ == '__main__':

    filename_1 = "./data/data2/1_hold_corners_1.csv"
    filename_2 = "./data/data2/1_hold_corners_1.csv"

    process(filename_1,filename_2,mode="hold")

    filename_3 = "./data/data2/3_read_corners_1.csv"
    filename_4 = "./data/data2/3_read_corners_1.csv"

    process(filename_3,filename_4,mode="read")

    filename_5 = "./data/data2/7_writeq_corners_1.csv"
    filename_6 = "./data/data2/8_writeqb_corners_1.csv"

    process(filename_5,filename_6,mode="write")


