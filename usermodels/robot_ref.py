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
        params['_init_start_'] = False

    ref_list = [
        (0.0, 0.0),#(1.25, 0.0),(2.5, 0.0),(3.75, 0.0),
        (5.0, 0.0),#(5.0, 1.25),(5.0, 2.5),(5.0, 3.75),
        (5.0, 5.0),#(3.75, 5.0),(2.5, 5.0),(1.25, 5.0),
        (0.0, 5.0),#(0.0, 3.75),(0.0, 2.5),(0.0, 1.25),
        (0.0, 0.0),
        (5.0, 0.0),#(5.0, 1.25),(5.0, 2.5),(5.0, 3.75),
        (5.0, 5.0),#(3.75, 5.0),(2.5, 5.0),(1.25, 5.0),
        (0.0, 5.0),#(0.0, 3.75),(0.0, 2.5),(0.0, 1.25),
        (0.0, 0.0)
    ]

    if params['pointer'] >= len(ref_list):
        x_ref = inputs[0][0]
        y_ref = inputs[0][1]
        th_ref = inputs[0][2]
        return {0: np.array((x_ref, y_ref, th_ref)), 1: np.array((0))}
    else:
        cont = np.array((1))

        x_pos = inputs[0][0]
        y_pos = inputs[0][1]

        x_ref = ref_list[params['pointer']][0]
        y_ref = ref_list[params['pointer']][1]
        th_ref = np.arctan2((y_ref - y_pos), (x_ref - x_pos))

        if np.sqrt((x_ref - x_pos) ** 2 + (y_ref - y_pos) ** 2) <= 0.05 and params['pointer'] < len(ref_list)-1:
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
        '_init_start_': True
    }
    return io_data, params
