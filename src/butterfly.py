# ======================================================================
# filename: butterfly.py
# author: ZhangShen
# email: colson_z@outlook.com
# time: 2021.01.11
# purpose: draw the butterfly using the csv files from the cadence
# ======================================================================
                                                    
from margin import *
from read import *

# ======================================================================
# Function name: multi_margin_find
# Usage: According to the input two sets of curves, 
#       using `zero` as the dividing line to search up and down 
#       respectively, calculate the corresponding margin
# Input: Curve_1_x, Curve_1_y, Curve_2_x, Curve_2_y: two sets of curves
#        big_small: search the max or min square ( 1-max 0-min )
#        sel: from the two areas sellect the min/max one (1-max 0-min)
#        search_ratio: Narrow down search range while finding the 
#                       writing margin
#        start, end, zero: the search range and the dividing line
#                          !!! can be the format list or single value
#        line_span: the searching span
#        search_step_size: Step size of recursive search
#        line_step_size: Step size of the line
# Return: The coordinates of the largest or smallest rectangle found 
#        and the corresponding margin
#         The curves of the butterfly
#         The square of the margin
# ======================================================================
def multi_margin_find(filename_q, filename_qb, mode="read", zeros=0, start=-1.2, end=1.2, line_span=1.2, auto_zero=False, auto_start=False, search_ratio=1.0):
    if mode == "read":
        big_small = 1
        sel = 0
    elif mode == "hold":
        big_small = 1
        sel = 0
    elif mode == "write":
        big_small = 0
        sel = 0
    else:
        big_small = 1
        sel = 0

    margin = []
    curve_1 = []
    curve_2 = []
    square = []
    
    datas_q  = Read_CSV(filename_q)
    datas_qb = Read_CSV(filename_qb)

    data_1_x, data_1_y, number = Data_Filter(datas_q)
    data_2_x, data_2_y, number = Data_Filter(datas_qb)

    Q_1  = data_1_x.copy()
    QB_1 = data_1_y.copy()
    Q_2  = data_2_y.copy()
    QB_2 = data_2_x.copy()

    length = len(Q_1)

    for i in range(length):
        if(auto_start or auto_zero):
            cross_point = intersection.intersection(Q_1[i],QB_1[i],Q_2[i],QB_2[i])
            length_crosspoint = len(cross_point[0])

        if type(zeros)!=list:
            the_zero = zeros
        else:
            the_zero = zeros[i]

        if(auto_zero):
            if(length_crosspoint==3):
                the_zero = cross_point[1][1] - cross_point[0][1]

        if type(start)!=list:
            the_start = start
        else:
            the_start = start[i]

        if(auto_start):
            if(length_crosspoint==3):
                the_start = cross_point[1][2] - cross_point[0][2]

        if type(end)!=list:
            the_end = end 
        else:
            the_end = end[i]

        # !!! you can modify the size to get more accurate result
        the_search_step_size = 0.01
        the_line_step_size = 0.01

        the_square, the_margin = margin_find(Q_1[i],QB_1[i],Q_2[i],QB_2[i],big_small=big_small,sel=sel, 
                                            zero=the_zero,start=the_start, end=the_end, line_span=line_span,
                                            search_ratio=search_ratio,search_step_size=the_search_step_size,line_step_size=the_line_step_size)
        if(the_square == False) :
            square.append([])
            margin.append( [] )    
        else:
            square.append(the_square)
            margin.append(the_margin)
        curve_1.append([Q_1[i],QB_1[i]])
        curve_2.append([Q_2[i],QB_2[i]])

    the_margins = []
    for i in margin:
        if(len(i)==0):
            the_margins.append(-1)
        else:
            the_margins.append( float(min(i)) )

    return the_margins,curve_1,curve_2,square