"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a drain-type function.

"""
import numpy as np

# Funcion principal (para la ejecución)
def drain_block(time, inputs, params):
    auxlist = params['mem']
    auxlist.append(inputs[0])
    params['mem'] = auxlist
    return {0: 0.0}

# Funcion para inicializar los datos y parámetros necesarios para el bloque
def _init_():
    """
    External function initialization data
    """
    io_data = {
        'run_ord': 3,
        'inputs': 1,
        'outputs': 0,
        'color': 'blue'
    } #. Dictionary with the block type, number of inputs and number of outputs.
    params = {} #. Dictionary with the necessary parameters for the function.
    return io_data, params
