"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a Z-process-type function used in "watertank.dat"

"""
import numpy as np

def sqrt_pcs(time, inputs, params):
    """
    External function 'sqrt_pcs'
    """
    return {0: np.array(np.sqrt(inputs[0]))}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 2,
        'inputs': 1,
        'outputs': 1,
        'color': (100, 255, 75)
    }
    params = {}
    return io_data, params
