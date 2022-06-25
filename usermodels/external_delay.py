"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a delay function used in "external_delay.dat"

"""
import numpy as np

# Funcion principal (para la ejecución)
# Must have the same time as the file
def external_delay(time, inputs, params):
    """
    External function 'external_delay'
    
    :param time: Time value for the main loop.
    :param inputs: Dictionary with all the input values
    :param params: Dictionary with all the necessary parameters for the function 
    :type time: float 
    :type inputs: dict{numpy.darray}
    :type params: dict{str}
    :return: Dictionary with the output(s) as float or numpy vector
    :rtype: dict{numpy.darray}
    """
    if params['_init_start_']:
        params['mem_list'] = [inputs[0]]
        aux_list = params['mem_list']
        params['_init_start_'] = False
    else:
        aux_list = params['mem_list']
        aux_list.append(inputs[0])
    if len(aux_list) > params['delay_len']+1:
        aux_list = aux_list[-(params['delay_len']+1):]
    params['mem_list'] = aux_list
    return {0: aux_list[0]}

#Funcion para inicializar los datos y parámetros necesarios para el bloque
def _init_():
    """
    External function initialization data
    """
    io_data = {
        'run_ord': 2,
        'inputs': 1,
        'outputs': 1,
        'color': 'aqua'
    } #. Dictionary with the block type, number of inputs and number of outputs.
    params = {
        '_init_start_': True,
        'delay_len': 10
    } #. Dictionary with the necessary parameters for the function.
    return io_data, params
