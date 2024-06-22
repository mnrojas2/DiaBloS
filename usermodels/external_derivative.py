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
    if params['_init_start_']:
        params['t_old'] = time
        params['i_old'] = inputs[0]
        params['didt_old'] = 0
        params['_init_start_'] = False
        return {0: 0.0}

    if time == params['t_old']:
        return {0: np.array(params['didt_old'])}
    
    dt = time - params['t_old']
    di = inputs[0] - params['i_old']
    didt = di / dt
    
    params['t_old'] = time
    params['i_old'] = inputs[0]
    params['didt_old'] = didt
    
    return {0: np.array(didt)}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 2,
        'inputs': 1,
        'outputs': 1,
        'color': 'aqua'
    }
    params = {
        '_init_start_': True
    }
    return io_data, params