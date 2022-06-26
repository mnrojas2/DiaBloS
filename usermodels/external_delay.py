"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a delay function used in "external_delay.dat"

"""

def external_delay(time, inputs, params):
    """
    External function 'external_delay'
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

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'run_ord': 2,
        'inputs': 1,
        'outputs': 1,
        'color': 'aqua'
    }
    params = {
        '_init_start_': True,
        'delay_len': 10
    }
    return io_data, params
