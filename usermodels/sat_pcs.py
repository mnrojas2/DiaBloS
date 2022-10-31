"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a source-type function used in "external_src_block.dat"

"""
import numpy as np

def sat_pcs(time, inputs, params):
    """
    External function 'sat_pcs'
    """
    if inputs[0] >= params['max']:
        return {0: np.array(params['max'])}
    elif inputs[0] <= params['min']:
        return {0: np.array(params['min'])}
    else:
        return {0: np.array(inputs[0])}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 2,
        'inputs': 1,
        'outputs': 1,
        'color': (25, 75, 100)
    }
    params = {
        'min': 0.0,
        'max': 2.0
    }
    return io_data, params
