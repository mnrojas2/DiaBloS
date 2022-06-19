"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example with a gain function. It only scale the input with the value it's set in the parameter 'gain'.

"""
import numpy as np

#Funcion principal (para la ejecución)
def external_rk45(time, inputs, params, output_only=False, next_add_in_memory=True, dtime=0.01):
    """
    External function 'external_rk45'
    
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
    if params['_init_start_'] == True:
        params['dtime'] = dtime
        params['mem'] = np.array(params['init_conds'])
        params['mem_list'] = [np.zeros(params['mem'].shape)]
        params['mem_len'] = 5.0  # Agregar otros largos dependiendo del metodo
        params['_init_start_'] = False

        params['nb_loop'] = 0
        params['RK45_Klist'] = [0, 0, 0, 0]  # K1, K2, K3, K4
        params['add_in_memory'] = True  # Para entregar valores de output_only al principio

    if output_only == True:
        old_add_in_memory = params['add_in_memory']
        params['add_in_memory'] = next_add_in_memory  # Actualizar para siguiente loop
        if old_add_in_memory == True:
            return {0: params['mem']}
        else:
            return {0: params['aux']}
    else:
        # Comprueba que los vectores de llegada tengan las mismas dimensiones que el vector memoria.
        if params['mem'].shape != inputs[0].shape:
            print("ERROR: Dimension Error in initial conditions in", params['_name_'])
            params['_init_start_'] = True
            return {'E': True}

        # Se entrega el valor antes de agregar, por lo que se guarda antes de cambiar
        mem_old = params['mem']

        # Runge-Kutta 45
        K_list = params['RK45_Klist']
        K_list[params['nb_loop']] = params['dtime'] * inputs[0]  # Calculo de K1, K2, K3 o K4
        params['RK45_Klist'] = K_list
        K1, K2, K3, K4 = K_list

        if params['nb_loop'] == 0:
            params['nb_loop'] += 1
            params['aux'] = np.array(params['mem'] + 0.5 * K1)
            return {0: params['aux']}
        elif params['nb_loop'] == 1:
            params['nb_loop'] += 1
            params['aux'] = np.array(params['mem'] + 0.5 * K2)
            return {0: params['aux']}
        elif params['nb_loop'] == 2:
            params['nb_loop'] += 1
            params['aux'] = np.array(params['mem'] + K3)
            return {0: params['aux']}
        elif params['nb_loop'] == 3:
            params['nb_loop'] = 0
            params['mem'] += (1 / 6) * (K1 + 2 * K2 + 2 * K3 + K4)

        aux_list = params['mem_list']
        aux_list.append(inputs[0])
        if len(aux_list) > params['mem_len']:  # 5 solo por probar, dependería del método de integración
            aux_list = aux_list[-5:]
        params['mem_list'] = aux_list

        return {0: mem_old}

#Funcion para inicializar los datos y parámetros necesarios para el bloque
def _init_():
    """
    External function initialization data
    """
    io_data = {
        'run_ord': 1,
        'inputs': 1,
        'outputs': 1,
        'color': 'magenta'
    } #. Dictionary with the block type, number of inputs and number of outputs.
    params = {
        'init_conds': 0.0,
        'method': 'RK45',
        '_init_start_': True
    } #. Dictionary with the necessary parameters for the function.
    return io_data, params

#cada archivo tiene 2 funciones, un ejecutable y un inicializador
#el nombre del archivo que sea igual al ejecutable o mejor al del bloque asignado (cambiar cuando se inicializa el nombre de la funcion)

#- el inicializador es unicamente para darle la información al programa de los datos ajustables para el bloque
#-- por ejemplo el nombre, el tipo, el numero de inputs y outputs

#- el ejecutable hace de funcion al momento de correr la simulacion/ejecucion
