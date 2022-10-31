"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a source-type function used in "external_src_block.dat"

"""
import numpy as np

def robot_torques(time, inputs, params):
    """
    External function 'robot_torques'
    """
    v0 = params['v0']
    w0 = params['w0']
    r = params['r']
    m = params['m']
    J = params['J']
    W = params['W']
    c = params['c']
    b = params['b']
    T = params['T']

    if time < T:
        t_right = v0*r*c/2
        t_left = v0*r*c/2
    elif time < 2 * T:
        t_right = w0 * b * r / W
        t_left = -w0 * b * r / W
    elif time < 3 * T:
        t_right = v0 * r * c / 2
        t_left = v0 * r * c / 2
    elif time < 4 * T:
        t_right = w0 * b * r / W
        t_left = -w0 * b * r / W
    elif time < 5 * T:
        t_right = v0 * r * c / 2
        t_left = v0 * r * c / 2
    elif time < 6 * T:
        t_right = w0 * b * r / W
        t_left = -w0 * b * r / W
    elif time < 7 * T:
        t_right = v0 * r * c / 2
        t_left = v0 * r * c / 2
    else: #time < 8 * T:
        t_right = w0 * b * r / W
        t_left = -w0 * b * r / W

    return {0: np.array(t_right),
            1: np.array(t_left)}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 0,
        'inputs': 0,
        'outputs': 2,
        'color': (50, 120, 60)
    }
    params = {
        'v0': 1,
        'w0': np.pi / 2,
        'r': 0.15,
        'm': 10,
        'J': 1,
        'W': 0.4,
        'c': 0.3,
        'b': 0.3,
        'T': 1.0
    }
    return io_data, params
