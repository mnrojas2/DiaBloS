"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a process-type function with multiple inputs and multiple outputs.

"""
import numpy as np

# Main function (executable in the simulation)
# This function must have the same name as the file
def mimo_block(time, inputs, params):
    """
    Main function
    """
    return {0: np.array(inputs[1]), 1: np.array(inputs[0])}

# Initialization function (to set function type, inputs, outputs and color and other parameters specific for the function)
def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 2,
        'inputs': 2,
        'outputs': 2,
        'color': 'orange'
    }                       #. Dictionary with the block type, number of inputs and outputs and color block.
    params = {}             #. Dictionary with the necessary parameters for the function.
    return io_data, params
