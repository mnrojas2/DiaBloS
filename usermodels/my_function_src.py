"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a source-type function used in "external_src_block.dat"

"""
import numpy as np

# Funcion principal (para la ejecución)
# Must have the same time as the file
def my_function_src(time, inputs, params):
    """
    External function 'my_function'
    
    :param time: Time value for the main loop.
    :param inputs: Dictionary with all the input values
    :param params: Dictionary with all the necessary parameters for the function 
    :type time: float 
    :type inputs: dict{numpy.darray}
    :type params: dict{str}
    :return: Dictionary with the output(s) as float or numpy vector
    :rtype: dict{numpy.darray}
    """
    return {0: np.array([params['value_1']]),
            1: np.array([params['value_2']])}

#Funcion para inicializar los datos y parámetros necesarios para el bloque
def _init_():
    """
    External function initialization data
    """
    io_data = {
        'run_ord': 0,
        'inputs': 0,
        'outputs': 2,
        'color': 'blue'
    } #. Dictionary with the block type, number of inputs and number of outputs.
    params = {
        'value_1': 1,
        'value_2': -1
    } #. Dictionary with the necessary parameters for the function.
    return io_data, params
