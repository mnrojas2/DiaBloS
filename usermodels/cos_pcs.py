"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a source-type function used in "robot.dat"

"""
import numpy as np

def cos_pcs(time, inputs, params):
    """
    External function 'my_function'
    """
    return {0: np.array(params['amplitude']*np.cos(params['omega']*inputs[0] + params['init_angle']))}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 2,
        'inputs': 1,
        'outputs': 1,
        'color': 'purple'
    }
    params = {
        'amplitude': 1.0,
        'omega': 1.0,
        'init_angle': 0.0
    }
    return io_data, params
