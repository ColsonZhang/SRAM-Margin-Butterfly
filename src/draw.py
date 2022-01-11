# ======================================================================
# filename: draw.py
# author: ZhangShen
# email: colson_z@outlook.com
# time: 2021.01.08
# purpose: draw the butterfly picture of SRAM's margin
# ======================================================================

import numpy as np
import matplotlib.pyplot as plt
from margin import *
from read import *


# ======================================================================
# Function name: margin_draw
# Usage: draw the butterfly
# Input: curve_1, curve_2 : the two curves of the butterfly diagram
#        square : the square of the margin
#        number : the number of the diagrams
#        titles : the titles of the multi-diagrams
#        draw_square: whether drawing the margin square
#        rows, columns: the rows and columns of the figure
# Return: the butterfly diagram
# ======================================================================
def margin_draw(curve_1, curve_2, square=[], number=1, titles=["margin"], draw_square=True, rows=1, columns=1):
    figsize = (2*columns,2*rows)
    fig, axs = plt.subplots(rows,columns, figsize=figsize)
    for i in range(number):
        if(rows==1):
            if(columns==1):
                the_ax = axs
            else:
                the_ax = axs[i]
        else:
            the_ax = axs[int((i)/columns)][i%columns]
        the_ax.plot(curve_1[i][0],curve_1[i][1])
        the_ax.plot(curve_2[i][0],curve_2[i][1])
        if(draw_square):
            for j in square[i]:
                the_ax.plot(j[0],j[1])
        the_ax.set_aspect('equal', 'box')
        the_ax.set_title(titles[i])

    plt.axis('scaled')
    plt.tight_layout()
    plt.show()  
