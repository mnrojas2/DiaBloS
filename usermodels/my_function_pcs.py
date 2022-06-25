"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a process-type function used in "external_pcs_block.dat"

"""
import numpy as np

# Funcion principal (para la ejecución)
# Must have the same time as the file
def my_function_pcs(time, inputs, params):
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
    return {0: np.array(params['gain']*inputs[0])}

#Funcion para inicializar los datos y parámetros necesarios para el bloque
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
        'gain': 1.5
    } #. Dictionary with the necessary parameters for the function.
    return io_data, params
