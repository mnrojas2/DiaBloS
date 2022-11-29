"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a source-type function used in "external_src_block.dat"

"""
import numpy as np

def robot_ref(time, inputs, params):
    """
    External function 'robot_ref'
    """
    if params['_init_start_']:
        params['pointer'] = 0

        Tp = params['interval']
        length = params['sq_length']
        lado = np.linspace(0, length, 1 + int(length / Tp))

        Tp_long = lado.shape[0]
        lado_a = np.array((lado, np.zeros(Tp_long))).T
        lado_b = np.array((length * np.ones(Tp_long), lado)).T
        lado_c = np.array((lado[::-1], length * np.ones(Tp_long))).T
        lado_d = np.array((np.zeros(Tp_long), lado[::-1])).T

        params['ref_list'] = np.concatenate((lado_a, lado_b, lado_c, lado_d))
        params['_init_start_'] = False

    ref_list = params['ref_list']

    cont = np.array((1))

    x_pos = inputs[0][0]
    y_pos = inputs[0][1]

    x_ref = ref_list[params['pointer']][0]
    y_ref = ref_list[params['pointer']][1]
    th_ref = np.arctan2((y_ref - y_pos), (x_ref - x_pos))

    if np.sqrt((x_ref - x_pos) ** 2 + (y_ref - y_pos) ** 2) <= params['interval']*0.25 and params['pointer'] < len(ref_list)-1:
        params['pointer'] += 1

    return {0: np.array((x_ref, y_ref, th_ref)), 1: cont}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 2,
        'inputs': 1,
        'outputs': 2,
        'color': (255, 12, 76)
    }
    params = {
        '_init_start_': True,
        'sq_length': 5,
        'interval': 0.25
    }
    return io_data, params
