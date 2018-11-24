# Author: Vanessa Fernandez Martinez

import numpy as np
import math


def highpassfilter(size, frec, n):

    x, y = np.ogrid[:size[0], :size[1]]
    cen_x, cen_y = size[0] / 2, size[1] / 2
    
    dis = np.sqrt((x - cen_x) ** 2 + (y - cen_y) ** 2)
    LPF = 1 / (1 + (dis / frec) **(2*n))

    # Calculate the high pass filter
    HPF = 1- LPF
    return HPF
