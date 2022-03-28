# Se deben agregar las librerias necesarias para correr la funcion en cada archivo
import numpy as np

#Funcion principal (para la ejecución)
def my_function(time, inputs, params):
    # Funcion ganancia
    return {0: np.array(params['gain']*inputs[0])}

#Funcion para inicializar los datos y parámetros necesarios para el bloque
def _init_():
    io_data = {
        'run_ord': 2,
        'inputs': 1,
        'outputs': 1,
    }
    params = {
        'gain': 1.5
    }
    return io_data, params

#cada archivo tiene 2 funciones, un ejecutable y un inicializador
#el nombre del archivo que sea igual al ejecutable o mejor al del bloque asignado (cambiar cuando se inicializa el nombre de la funcion)

#- el inicializador es unicamente para darle la información al programa de los datos ajustables para el bloque
#-- por ejemplo el nombre, el tipo, el numero de inputs y outputs

#- el ejecutable hace de funcion al momento de correr la simulacion/ejecucion
