"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a source-type function used in "external_src_block.dat"

"""
import numpy as np

def ode_exact_crit(time, inputs, params):
    """
    External function 'my_function'
    """
    return {0: np.array((1-np.cos(time), np.sin(time)))}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 0,
        'inputs': 0,
        'outputs': 1,
        'color': (255,45,56)
    }
    params = {}
    return io_data, params
