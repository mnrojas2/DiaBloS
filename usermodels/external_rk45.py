"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a RK45 integrator function used in "external_integrator.dat"

"""
import numpy as np

def external_rk45(time, inputs, params, output_only=False, next_add_in_memory=True, dtime=0.01):
    """
    External function 'external_rk45'
    """
    if params['_init_start_'] == True:
        params['dtime'] = dtime
        params['mem'] = np.array(params['init_conds'])
        params['mem_list'] = [np.zeros(params['mem'].shape)]
        params['mem_len'] = 5.0
        params['_init_start_'] = False

        params['nb_loop'] = 0
        params['RK45_Klist'] = [0, 0, 0, 0]  # K1, K2, K3, K4
        params['add_in_memory'] = True  # For output_only purposes

    if output_only == True:
        old_add_in_memory = params['add_in_memory']
        params['add_in_memory'] = next_add_in_memory  # Update for next loop
        if old_add_in_memory == True:
            return {0: params['mem']}
        else:
            return {0: params['aux']}
    else:
        # Check that the arrival vectors have the same dimensions as the memory vector.
        if params['mem'].shape != inputs[0].shape:
            print("ERROR: Dimension Error in initial conditions in", params['_name_'])
            params['_init_start_'] = True
            return {'E': True}

        # Value is saved before it gets changed by the following lines
        mem_old = params['mem']

        # Runge-Kutta 45
        K_list = params['RK45_Klist']
        K_list[params['nb_loop']] = params['dtime'] * inputs[0]  # K1, K2, K3 or K4
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
        if len(aux_list) > params['mem_len']:
            aux_list = aux_list[-5:]
        params['mem_list'] = aux_list

        return {0: mem_old}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 1,
        'inputs': 1,
        'outputs': 1,
        'color': 'magenta'
    }
    params = {
        'init_conds': 0.0,
        'method': 'RK45',
        '_init_start_': True
    }
    return io_data, params
