"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a source-type function.

"""
import numpy as np

# Main function (executable in the simulation)
# This function must have the same name as the file
def source_block(time, inputs, params):
    return {0: np.array([params['value']])}

# Initialization function (to set function type, inputs, outputs and color and other parameters specific for the function)
def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 0,
        'inputs': 0,
        'outputs': 1,
        'color': 'blue'
    }                       #. Dictionary with the block type, number of inputs and number of outputs.
    params = {
        'value': 1
    }                       #. Dictionary with the necessary parameters for the function.
    return io_data, params
