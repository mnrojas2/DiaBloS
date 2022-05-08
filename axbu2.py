# Se deben agregar las librerias necesarias para correr la funcion en cada archivo
import numpy as np

#Funcion principal (para la ejecución)
def axbu2(time, inputs, params):
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
        'run_ord': 2
    }
    params = {}
    return io_data, params

#cada archivo tiene 2 funciones, un ejecutable y un inicializador
#el nombre del archivo que sea igual al ejecutable o mejor al del bloque asignado (cambiar cuando se inicializa el nombre de la funcion)

#- el inicializador es unicamente para darle la información al programa de los datos ajustables para el bloque
#-- por ejemplo el nombre, el tipo, el numero de inputs y outputs

#- el ejecutable hace de funcion al momento de correr la simulacion/ejecucion
