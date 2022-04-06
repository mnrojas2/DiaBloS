# Se deben agregar las librerias necesarias para correr la funcion en cada archivo
import numpy as np

#Funcion principal (para la ejecución)
def my_function2(time, inputs, params, output_only=False, dtime=0.01):
    # Funcion integrador
    if params['_init_start_'] == True:
        params['dtime'] = dtime
        params['mem'] = np.array(params['init_conds'])
        params['mem_list'] = [np.zeros(params['mem'].shape)]
        params['mem_len'] = 5.0  # Agregar otros largos dependiendo del metodo
        params['_init_start_'] = False

    if output_only == True:
        return {0: params['mem']}
    else:
        if params['mem'].shape != inputs[0].shape:
            print("ERROR: Dimension Error in initial conditions in", params['_name_'])
            return {'E': True}

        if params['method'] == 'FWD_RECT':
            params['mem'] += params['dtime'] * inputs[0]
        elif params['method'] == 'BWD_RECT':
            params['mem'] += params['dtime'] * params['mem_list'][-1]
        elif params['method'] == 'TUSTIN':
            params['mem'] += 0.5 * params['dtime'] * (inputs[0] + params['mem_list'][-1])

        aux_list = params['mem_list']
        aux_list.append(inputs[0])
        if len(aux_list) > params['mem_len']:  # 5 solo por probar, dependería del método de integración
            aux_list = aux_list[-5:]
        params['mem_list'] = aux_list

        return {0: params['mem']}

#Funcion para inicializar los datos y parámetros necesarios para el bloque
def _init_():
    io_data = {
        'inputs': 1,
        'outputs': 1,
        'run_ord': 1
    }
    params = {
        'init_conds': 1.0,
        'method': 'FWD_RECT',
        '_init_start_': True
    }
    return io_data, params

#cada archivo tiene 2 funciones, un ejecutable y un inicializador
#el nombre del archivo que sea igual al ejecutable o mejor al del bloque asignado (cambiar cuando se inicializa el nombre de la funcion)

#- el inicializador es unicamente para darle la información al programa de los datos ajustables para el bloque
#-- por ejemplo el nombre, el tipo, el numero de inputs y outputs

#- el ejecutable hace de funcion al momento de correr la simulacion/ejecucion
