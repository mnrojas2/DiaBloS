"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a source-type function used in "external_src_block.dat"

"""
import numpy as np

def robot_cpos(time, inputs, params):
    """
    External function 'robot_cpos'
    """
    errors = inputs[0]
    e_x = errors[0]
    e_y = errors[1]
    e_theta = errors[2]
    return {0: np.array((0, 0))}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 2,
        'inputs': 1,
        'outputs': 1,
        'color': (120, 35, 85)
    }
    params = {
        'kx': 1.0,
        'ky': 1.0,
        'kth': 1.0
    }
    return io_data, params
