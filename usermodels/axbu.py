"""
Python module for external functions

#. WARNING: You must add all the necessary libraries here to make the function work in the main loop.
#. This file includes an example for a linealized dynamic system used in "feedback-three_methods.dat".

"""

# Se deben agregar las librerias necesarias para correr la funcion en cada archivo
import numpy as np

# Funcion principal (para la ejecución)
# Must have the same time as the file
def axbu(time, inputs, params):
    # Excepciones
    if inputs[1].shape != (2,) or inputs[0] != ():
        print("ERROR: Vector dimensions don't match")
        return {'E': True}

    # Funcion Ax + Bu
    A = np.array([[0, 1], [-1, -0.4]])
    B = np.array([0, 1])
    sol = np.dot(A, inputs[1]) + np.dot(B, inputs[0])
    return {0: sol}

#Funcion para inicializar los datos y parámetros necesarios para el bloque
def _init_():
    io_data = {
        'inputs': 2,
        'outputs': 1,
        'run_ord': 2,
        'color': 'green'
    }
    params = {}
    return io_data, params
