"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a source-type function used in "external_src_block.dat"

"""
import numpy as np

def square_robot(time, inputs, params):
    """
    External function 'square_robot'
    """
    i = int(100*time)

    if i < 50:
        u0 = np.array([1.95, 1.95])
    elif i < 160:
        u0 = np.zeros(2)
    elif i < 210:
        u0 = np.array([-1.85, -1.85])

    # theta: 0 to pi/2
    elif i < 290:
        u0 = np.array([1.05, -1.05])
    elif i < 350:
        u0 = np.array([-1.05, 1.05])

    # y: 0 to 2m
    elif i < 400:
        u0 = np.array([1.95, 1.95])
    elif i < 510:
        u0 = np.zeros(2)
    elif i < 560:
        u0 = np.array([-1.9, -1.9])

    # theta: pi/2 to pi
    elif i < 630:
        u0 = np.array([1.05, -1.05])
    elif i < 680:
        u0 = np.array([-1.025, 1.025])

    # x: 2 to 0m
    elif i < 730:
        u0 = np.array([1.95, 1.95])
    elif i < 850:
        u0 = np.zeros(2)
    elif i < 900:
        u0 = np.array([-1.85, -1.85])

    # theta: pi to (3/2)*pi
    elif i < 970:
        u0 = np.array([1.05, -1.05])
    elif i < 1030:
        u0 = np.array([-1.025, 1.025])

    # y: 2 to 0m
    elif i < 1080:
        u0 = np.array([1.95, 1.95])
    elif i < 1200:
        u0 = np.zeros(2)
    elif i < 1250:
        u0 = np.array([-1.85, -1.85])
    else:
        u0 = np.zeros(2)

    return {0: u0[0],
            1: u0[1]}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 0,
        'inputs': 0,
        'outputs': 2,
        'color': (50, 120, 60)
    }
    params = {}
    return io_data, params
