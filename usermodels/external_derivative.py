"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a derivative function used in "external_derivator.dat"

"""
import numpy as np

def external_derivative(time, inputs, params):
    """
    External function 'external_derivative'
    """
    # Funcion integrador
    if params['_init_start_']:
        params['t_old'] = time
        params['i_old'] = inputs[0]
        params['_init_start_'] = False
        return {0: 0.0}
    dt = time - params['t_old']
    di = inputs[0] - params['i_old']
    params['t_old'] = time
    params['i_old'] = inputs[0]
    return {0: np.array(di / dt)}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'run_ord': 2,
        'inputs': 1,
        'outputs': 1,
        'color': 'aqua'
    }
    params = {
        '_init_start_': True
    }
    return io_data, params