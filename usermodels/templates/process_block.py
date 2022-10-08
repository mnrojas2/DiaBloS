"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a process-type function.

"""
import numpy as np

# Main function (executable in the simulation)
# This function must have the same name as the file
def process_block(time, inputs, params):
    """
    Main function
    """
    return {0: np.array(params['gain']*inputs[0])}

# Initialization function (to set function type, inputs, outputs and color and other parameters specific for the function)
def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 2,
        'inputs': 1,
        'outputs': 1,
        'color': 'orange'
    }                       #. Dictionary with the block type, number of inputs and number of outputs.
    params = {
        'gain': 1
    }                       #. Dictionary with the necessary parameters for the function.
    return io_data, params
