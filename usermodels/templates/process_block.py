"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a process-type function.

"""
import numpy as np

# Funcion principal (para la ejecución)
def process_block(time, inputs, params):
    return {0: np.array(params['gain']*inputs[0])}

# Funcion para inicializar los datos y parámetros necesarios para el bloque
def _init_():
    """
    External function initialization data
    """
    io_data = {
        'run_ord': 2,
        'inputs': 1,
        'outputs': 1,
        'color': 'orange'
    } #. Dictionary with the block type, number of inputs and number of outputs.
    params = {
        'gain': 1
    } #. Dictionary with the necessary parameters for the function.
    return io_data, params
