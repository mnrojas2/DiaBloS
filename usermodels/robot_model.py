"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a source-type function used in "external_src_block.dat"

"""
import numpy as np

def robot_model(time, inputs, params):
    """
    External function 'sat_pcs'
    """
    tq_r = inputs[0]  # torque r
    tq_l = inputs[1]  # torque l
    st = inputs[2] # vector x

    xp = st[3]*np.cos(st[2])
    yp = st[3]*np.sin(st[2])
    op = st[4]
    vp = 1/(params['m']*params['r'])*(tq_r + tq_l) - params['c']/params['m']*st[3]
    wp = params['W']/(2*params['J']*params['r'])*(tq_r - tq_l) - params['b']/params['J']*st[4]

    return {0: np.array((xp, yp, op, vp, wp))}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 2,
        'inputs': 3,
        'outputs': 1,
        'color': (25, 75, 150)
    }
    params = {
        'L': 0.6,
        'W': 0.4,
        'H': 0.15,
        'r': 0.15,
        'm': 10,
        'J': 1,
        'c': 0.3,
        'b': 0.3
    }
    return io_data, params
