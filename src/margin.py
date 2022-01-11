# ======================================================================
# filename: margin.py
# author: ZhangShen
# email: colson_z@outlook.com
# time: 2021.01.09
# purpose: find the sram margin using the csv files from the simulation
# ======================================================================

import numpy as np
import intersection


# ======================================================================
# Function name: get_line
# Usage:    generate data points: y = x + offset_y 
#           Note !!! x>0 and -span < y < span
# Input:    offset_y: offset in y-axis;
#           span: max range in y-axis
# Return: x,y points generated according to the rules
# ======================================================================
def get_line(offset_y, span = 1.3, line_step_size=0.01):
    if offset_y>0:
        x = np.linspace(0, span-offset_y, round((span-offset_y)/line_step_size))
    else :
        x = np.linspace(-offset_y, span, round((span+offset_y)/line_step_size))
    y = offset_y + x
    return x,y


# ======================================================================
# Function name: get_square
# Usage: find the max or min square, which can be contained 
#        by the two curves
# Input: Curve_1_x, Curve_1_y, Curve_2_x, Curve_2_y: two curves
#        start, end: the range of the offset in y-axis
#        line_span: the scan span 
#        big_small: search the max or min square ( 1-max 0-min )
#        search_step_size: Step size of recursive search
#        line_step_size: Step size of the line
# Return: the points and the area of the square found
# ======================================================================
def get_square(Curve_1_x, Curve_1_y, Curve_2_x, Curve_2_y, start=-1.2, end=1.2, line_span=1.2, big_small=1, search_step_size = 0.01, line_step_size = 0.01):
    square_x = []
    square_y = []
    # max_offset = 0
    # line_span = max( abs(start), abs(end) )

    if big_small == 1 :
        # find max square
        ref_square = 0
    else :
        # find min square
        ref_square = float("inf")
    
    #  different offset of y-axis between start and end
    for i in np.linspace(start,end,round((end-start)/search_step_size)+1):
        # get the line: y = x + i
        line_x, line_y = get_line(i, span=line_span, line_step_size=line_step_size )
        try:
            # get the intersection
            x1, y1 = intersection.intersection(line_x,line_y,Curve_1_x,Curve_1_y)
            x2, y2 = intersection.intersection(line_x,line_y,Curve_2_x,Curve_2_y)

            cross_x = [x1,x2]
            cross_y = [y1,y2]

            # get the square
            square_term = 0.5*((cross_x[0]-cross_x[1])**2 + (cross_y[0]-cross_y[1])**2)

            # judge the square
            if big_small == 1:
                if square_term > ref_square :
                    # print(square_term)
                    ref_square = square_term
                    # max_offset = i
                    square_x = cross_x
                    square_y = cross_y
            else :
                if square_term < ref_square :
                    # print(square_term)
                    ref_square = square_term
                    # max_offset = i
                    square_x = cross_x
                    square_y = cross_y 
        except:
            False, False, False
        
    return square_x, square_y, ref_square

# ======================================================================
# Function name: margin_find
# Usage: According to the input two sets of curves, 
#       using `zero as the dividing line to search up and down 
#       respectively, calculate the corresponding margin
# Input: Curve_1_x, Curve_1_y, Curve_2_x, Curve_2_y: two sets of curves
#        big_small: search the max or min square ( 1-max 0-min )
#        sel: from the two areas sellect the min/max one (1-max 0-min)
#        search_ratio: Narrow down search range while finding the 
#                       writing margin
#        start, end, zero: the search range and the dividing line
#        line_span: the searching span
#        search_step_size: Step size of recursive search
#        line_step_size: Step size of the line
# Return: The coordinates of the largest or smallest rectangle found 
#        and the corresponding margin
# ======================================================================
def margin_find(Curve_1_x,Curve_1_y,Curve_2_x,Curve_2_y,big_small=1,sel=0, search_ratio=0.6, start=-1.2, end=1.2, zero=0, line_span=1.2, search_step_size=0.01, line_step_size = 0.01):

    if(big_small == 0):
        cross_x, cross_y = intersection.intersection(Curve_1_x,Curve_1_y,Curve_2_x,Curve_2_y)
        offset_end = np.abs(cross_y[0] - cross_x[0])
        # multipy the search_ratio to avoid mismatch
        offset_end = offset_end*search_ratio
        end = offset_end

        y_1 = min(Curve_1_y)
        x_1 = Curve_1_x[ Curve_1_y.index(y_1) ]
        y_2 = min(Curve_2_x)
        x_2 = Curve_2_y[ Curve_2_x.index(y_2) ]

        if( y_1 < y_2 ):
            start = -np.abs(x_1 - y_1)
        else:
            start = -np.abs(x_2 - y_2)

    margin_square = []
    margin_area = []
    
    square_x,square_y,area    = get_square(Curve_1_x,Curve_1_y,Curve_2_x,Curve_2_y,start=start,end=zero, line_span=line_span, big_small=big_small,search_step_size=search_step_size, line_step_size =line_step_size)
    square_x2,square_y2,area2 = get_square(Curve_1_x,Curve_1_y,Curve_2_x,Curve_2_y,start=zero ,end=end, line_span=line_span ,big_small=big_small,search_step_size=search_step_size, line_step_size =line_step_size)
    
    if(square_x == False) or (square_x2 == False):
        return False, False

    if(len(square_x)==0) or (len(square_x2)==0):
        return False, False

    square_plot_X = [ square_x[0],square_x[1],square_x[1],square_x[0],square_x[0] ]
    square_plot_y = [ square_y[0],square_y[0],square_y[1],square_y[1],square_y[0] ] 

    square_plot_X2 = [ square_x2[0],square_x2[1],square_x2[1],square_x2[0],square_x2[0] ]
    square_plot_y2 = [ square_y2[0],square_y2[0],square_y2[1],square_y2[1],square_y2[0] ]
    
    if abs(area2-area)<1e-4:
        margin_square.append([square_plot_X,square_plot_y])
        margin_area.append(np.sqrt(area))
        margin_square.append([square_plot_X2,square_plot_y2])
        margin_area.append(np.sqrt(area2))
    elif area2 > area:
        # from the two areas sellect the min one
        if sel == 0:
            margin_square.append([square_plot_X,square_plot_y])
            margin_area.append(np.sqrt(area))
        else:
            margin_square.append([square_plot_X2,square_plot_y2])
            margin_area.append(np.sqrt(area2))
    else:
        # from the two areas sellect the min one
        if sel == 0:
            margin_square.append([square_plot_X2,square_plot_y2])
            margin_area.append(np.sqrt(area2))
        else:
            margin_square.append([square_plot_X,square_plot_y])
            margin_area.append(np.sqrt(area))

    return margin_square,margin_area


