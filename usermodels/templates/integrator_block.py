"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a integrator-type function.

"""
import numpy as np

# Funcion principal (para la ejecución)
def integrator_block(time, inputs, params, output_only=False, next_add_in_memory=True, dtime=0.01):
    
    if params['_init_start_'] == True:
        params['dtime'] = dtime
        params['mem'] = np.array(params['init_conds'])
        params['_init_start_'] = False

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

        # Forward euler
            if params['method'] == 'FWD_RECT':
                if params['add_in_memory']:
                    params['mem'] += params['dtime'] * inputs[0]
                else:
                    params['aux'] = np.array(params['mem'] + 0.5 * params['dtime'] * inputs[0])
                    return {0: params['aux']}
        return {0: mem_old}

# Funcion para inicializar los datos y parámetros necesarios para el bloque
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
