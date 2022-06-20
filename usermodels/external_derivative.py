"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example with a gain function. It only scale the input with the value it's set in the parameter 'gain'.

"""
import numpy as np

#Funcion principal (para la ejecución)
def external_derivative(time, inputs, params):
    """
    External function 'external_derivative'
    
    :param time: Time value for the main loop.
    :param inputs: Dictionary with all the input values
    :param params: Dictionary with all the necessary parameters for the function 
    :type time: float 
    :type inputs: dict{numpy.darray}
    :type params: dict{str}
    :return: Dictionary with the output(s) as float or numpy vector
    :rtype: dict{numpy.darray}
    """
    # Funcion integrador
    if params['_init_start_']:
        params['t_old'] = time
        params['i_old'] = inputs[0]
        params['_init_start_'] = False
        return {0: 0.0}
    dt = time - params['t_old']
    di = inputs[0] - params['i_old']
    params['t_old'] = time
    params['i_old'] = inputs[0]
    return {0: np.array(di / dt)}

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
        '_init_start_': True
    } #. Dictionary with the necessary parameters for the function.
    return io_data, params

#cada archivo tiene 2 funciones, un ejecutable y un inicializador
#el nombre del archivo que sea igual al ejecutable o mejor al del bloque asignado (cambiar cuando se inicializa el nombre de la funcion)

#- el inicializador es unicamente para darle la información al programa de los datos ajustables para el bloque
#-- por ejemplo el nombre, el tipo, el numero de inputs y outputs

#- el ejecutable hace de funcion al momento de correr la simulacion/ejecucion
