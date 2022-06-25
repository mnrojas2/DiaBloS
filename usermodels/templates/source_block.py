"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a source-type function.

"""
import numpy as np

# Funcion principal (para la ejecución)
def my_function_src(time, inputs, params):
    return {0: np.array([params['value']])}

# Funcion para inicializar los datos y parámetros necesarios para el bloque
def _init_():
    """
    External function initialization data
    """
    io_data = {
        'run_ord': 0,
        'inputs': 0,
        'outputs': 1,
        'color': 'blue'
    } #. Dictionary with the block type, number of inputs and number of outputs.
    params = {
        'value': 1
    } #. Dictionary with the necessary parameters for the function.
    return io_data, params
