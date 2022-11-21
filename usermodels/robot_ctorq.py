"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a source-type function used in "external_src_block.dat"

"""
import numpy as np

def robot_ctorq(time, inputs, params):
    """
    External function 'robot_ctorq'
    """
    return {0: np.array((1)), 1: np.array((1))}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 2,
        'inputs': 1,
        'outputs': 2,
        'color': (85, 35, 120)
    }
    params = {
        'kp': 10.0,
        'ki': 5.0
    }
    return io_data, params
