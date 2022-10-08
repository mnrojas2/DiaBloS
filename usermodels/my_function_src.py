"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a source-type function used in "external_src_block.dat"

"""
import numpy as np

def my_function_src(time, inputs, params):
    """
    External function 'my_function'
    """
    return {0: np.array([params['value_1']]),
            1: np.array([params['value_2']])}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 0,
        'inputs': 0,
        'outputs': 2,
        'color': 'blue'
    }
    params = {
        'value_1': 1,
        'value_2': -1
    }
    return io_data, params
