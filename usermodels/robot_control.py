"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a Z-process-type function used in "robot.dat"

"""
import numpy as np

def robot_control(time, inputs, params):
    """
    External function 'robot_control'
    """
    if params['_init_start_']:
        params['dtime'] = 0.01
        params['eth_old'] = 0
        params['_init_start_'] = False

    x_pos = inputs[0][0]
    y_pos = inputs[0][1]
    th_pos = inputs[0][2]

    x_ref = inputs[1][0]
    y_ref = inputs[1][1]
    th_ref = inputs[1][2]

    e_th = th_ref - th_pos
    e_th = (e_th + np.pi) % (2*np.pi) - np.pi

    d_eth = (e_th - params['eth_old']) / params['dtime']

    tau = params['kp_th'] * e_th + params['kd_th'] * d_eth
    fz = params['kp_dist'] * np.sqrt((x_ref - x_pos) ** 2 + (y_ref - y_pos) ** 2)

    tau_r = (fz / 2 + tau / params['W']) * params['r']
    tau_l = (fz / 2 - tau / params['W']) * params['r']
    
    if '_skip_' in params.keys() and params['_skip_']:
        params['_skip_'] = False
        return {0: np.array((tau_r)), 1: np.array((tau_l))}
    params['eth_old'] = e_th
    return {0: np.array((tau_r)), 1: np.array((tau_l))}

def _init_():
    """
    External function initialization data
    """
    io_data = {
        'b_type': 2,
        'inputs': 2,
        'outputs': 2,
        'color': (85, 35, 120)
    }
    params = {
        '_init_start_': True,
        'W': 0.4,
        'r': 0.15,
        'kp_dist': 20.0,
        'kp_th': 25.0,
        'kd_th': 40.0,
        'dtime': 0.01
    }
    return io_data, params
