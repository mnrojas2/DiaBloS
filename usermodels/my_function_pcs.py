"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a process-type function used in "external_pcs_block.dat"

"""
import numpy as np

def my_function_pcs(time, inputs, params):
    """
    External function 'my_function'
    """
    return {0: np.array(params['gain']*inputs[0])}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 2,
        'inputs': 1,
        'outputs': 1,
        'color': 'orange'
    }
    params = {
        'gain': 1.5
    }
    return io_data, params
