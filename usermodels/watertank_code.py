"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a linealized dynamic system used in "feedback-three_methods.dat".

"""

import numpy as np

def watertank_code(time, inputs, params):
    # Excepciones
    if inputs[1].shape != (2,) or inputs[0] != ():
        print("ERROR: Vector dimensions don't match")
        return {'E': True}

    c1 = 0.318
    c2 = 0.0001
    g = 9.81

    Kp = 10.0
    Ki = 55.0

    xd = c1 * inputs[1][1] - c2 * np.sqrt(2*g*np.abs(inputs[1][0]))
    ud = -Kp * xd + Ki * (inputs[0] - inputs[1][0])
    return {0: np.array([xd, ud])}

def _init_():
    io_data = {
        'inputs': 2,
        'outputs': 1,
        'b_type': 2,
        'color': (25, 220, 128)
    }
    params = {}
    return io_data, params
