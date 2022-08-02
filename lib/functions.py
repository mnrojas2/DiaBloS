"""
functions.py - Contains all the functions associated with the blocks in the simulation
"""

import numpy as np


class FunctionsCall:
    """
    Class to contain all the default functions available to work with in the simulation interface
    """

    def step(self, time, inputs, params):
        """
        Step source function

        :purpose: Funcion que retorna un valor constante en el tiempo.
        :description: Esta es una funcion tipo fuente, la cual es piecewise. Se puede utilizar para indicar el inicio o término de una rama de un grafo.
        :param time: Valor que indica el período actual de simulación.
        :param inputs: Diccionario que entrega uno o más entradas para la función (si aplica).
        :param params['value']: El valor que la función retorna. Puede ser un escalar (float) como también un vector ([float, ...]).
        :param params['delay']: Indica un punto en el tiempo donde sucede el salto del piecewise.
        :param params['type']: ['up'/'down'] Indica si el salto es hacia arriba ('value') o hacia abajo (0).
        :param params['_name_']: Parámetro auxiliar entregado por el bloque asociado, para identificación de errores.
        :type time: float
        :type inputs: dict
        :type params['value']: float/numpy.ndarray
        :type params['delay']: float
        :type params['type']: str
        :type params['_name_']: str
        :return: El valor definido en 'value' o 0.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: notes
        :limitations: limitations
        :bugs: bugs

        """
        if params['type'] == 'up':
            change = True if time < params['delay'] else False
        elif params['type'] == 'down':
            change = True if time > params['delay'] else False
        else:
            print("ERROR: 'type' not correctly defined in", params['_name_'])
            return {'E': True}

        if change:
            return {0: 0*abs(np.array(params['value']))}
        else:
            return {0: np.array(params['value'])}

    def ramp(self, time, inputs, params):
        """
        Ramp source function

        :purpose: Funcion que retorna un valor que cambia linealmente en el tiempo.
        :description: Esta es una funcion tipo fuente, la cual es piecewise. El valor cambia en el tiempo de forma lineal, pudiendo este aumentar o disminuir.
        :param time: Valor que indica el período actual de simulación.
        :param inputs: Diccionario que entrega uno o más entradas para la función (si aplica).
        :param params['slope']: El valor de la pendiente que la función utiliza para entregar el resultado.
        :param params['delay']: Indica un punto en el tiempo donde sucede el inicio de la rampa.
        :type time: float
        :type inputs: dict
        :type params['slope']: float
        :type params['delay']: float
        :return: El valor de la pendiente multiplicado por la diferencia entre 'time' y 'delay'.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: notes
        :limitations: limitations
        :bugs: bugs

        """
        if params['slope'] == 0:
            return {0: 0}
        elif params['slope'] > 0:
            return {0: np.maximum(0, params['slope']*(time - params['delay']))}
        elif params['slope'] < 0:
            return {0: np.array(np.minimum(0, params['slope'] * (time - params['delay'])))}

    def sine(self, time, inputs, params):
        """
        Sinusoidal source function

        :purpose: Funcion que retorna una sinusoidal en el tiempo.
        :description: Esta es una funcion tipo fuente. Retorna una sinusoidal con variación en los parámetros de amplitud, frecuencia y ángulo inicial.
        :param time: Valor que indica el período actual de simulación.
        :param inputs: Diccionario que entrega uno o más entradas para la función (si aplica).
        :param params['amplitude']: Valor de amplitud que toma la sinusoidal.
        :param params['omega']: Valor en rad/s (2*pi*f) de la frecuencia que toma la sinusoidal.
        :param params['init_angle']: Valor en radianes del ángulo que toma la sinusoidal en tiempo cero.
        :type time: float
        :type inputs: dict
        :type params['amplitude']: float
        :type params['omega']: float
        :type params['init_angle']: float
        :return: Una sinusoidal de amplitud 'amplitude', frecuencia 'omega' y ángulo inicial 'init_angle'.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: notes
        :limitations: limitations
        :bugs: bugs

        """
        return {0: np.array(params['amplitude']*np.sin(params['omega']*time + params['init_angle']))}

    def noise(self, time, inputs, params):
        """
        Normal noise function

        :purpose: Funcion retorna un ruido aleatorio normal.
        :description: Esta es una funcion tipo fuente. Produce un valor aleatorio normal de media mu y varianza sigma**2.
        :param time: Valor que indica el período actual de simulación.
        :param inputs: Diccionario que entrega uno o más entradas para la función (si aplica).
        :param params['mu']: Valor de media del ruido.
        :param params['sigma']: Valor de desviación estándar del ruido.
        :type time: float
        :type inputs: dict
        :type params['sigma']: float
        :type params['mu']: float
        :return: Valor aleatorio normal de media mu y varianza sigma**2.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: notes
        :limitations: limitations
        :bugs: bugs

        """
        return {0: np.array(params['sigma'] ** 2 * np.random.randn() + params['mu'])}

    def gain(self, time, inputs, params):
        """
        Gain function

        :purpose: Funcion que escala una entrada por un factor.
        :description: Esta es una funcion tipo proceso. Retorna la misma entrada, pero escalada por un factor definido por el usuario. Esta entrada puede ser tanto escalar como vectorial, así como el factor de escalamiento.
        :param time: Valor que indica el período actual de simulación.
        :param inputs: Diccionario que entrega uno o más entradas para la función (si aplica).
        :param params['gain']: Valor de escalamiento de la entrada. Puede ser un valor escalar, o una matriz (solo para multiplicación vectorial).
        :type time: float
        :type inputs: dict
        :type params['gain']: float/numpy.ndarray
        :return: El valor de entrada, escalado por el factor 'gain'.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: notes
        :limitations: limitations
        :bugs: bugs

        """
        return {0: np.array(np.dot(params['gain'], inputs[0]))}

    def exponential(self, time, inputs, params):
        """
        Exponential function

        :purpose: Funcion que retorna el valor de una exponencial a partir de una entrada.
        :description: Esta es una funcion tipo proceso. Toma el valor de entrada, y le calcula la exponencial de la misma, con factores de escala para la base como al exponente.
        :param time: Valor que indica el período actual de simulación.
        :param inputs: Diccionario que entrega uno o más entradas para la función (si aplica).
        :param params['a']: Factor de escalamiento para la base de la exponencial.
        :param params['b']: Factor de escalamiento para el exponente de la exponencial.
        :type time: float
        :type inputs: dict
        :type params['a']: float
        :type params['b']: float
        :return: La exponencial del valor de la entrada.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: notes
        :limitations: limitations
        :bugs: bugs

        """
        return {0: np.array(params['a']*np.exp(params['b']*inputs[0]))}

    def sumator(self, time, inputs, params):
        """
        Sumator function

        :purpose: Funcion que retorna la suma de dos o más entradas.
        :description: Esta es una funcion tipo proceso. Toma cada valor de entrada y este lo asocia a un signo (positivo o negativo), para luego irlos sumando o restando en una variable auxiliar. La función soporta tanto operatoria escalar como vectorial.
        :param time: Valor que indica el período actual de simulación.
        :param inputs: Diccionario que entrega uno o más entradas para la función (si aplica).
        :param params['sign']: String que contiene todos los signos asociados a cada valor (o vector) de entrada. Cabe destacar que en caso de tener menos símbolos que vectores, la función asumirá que estos restantes sumarán.
        :param params['_name_']: Parámetro auxiliar entregado por el bloque asociado, para identificación de errores.
        :type time: float
        :type inputs: dict
        :type params['sign']: str
        :type params['_name_']: str
        :return: La suma de todas las entradas.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: Esta función retorna 'Error' si es que las dimensiones de alguna de las entradas no son iguales.
        :limitations: limitations
        :bugs: bugs

        """
        for i in range(len(inputs)-1):
            if inputs[i].shape != inputs[i+1].shape:
                print("ERROR: Dimensions don't fit in", params['_name_'])
                return {'E': True}

        if len(params['sign']) < len(inputs):
            params['sign'] += (len(inputs)-len(params['sign']))*'+'

        suma = np.zeros(inputs[0].shape)
        for i in range(len(inputs)):
            if params['sign'][i] == '+':
                suma += inputs[i]
            elif params['sign'][i] == '-':
                suma -= inputs[i]
            else:
                print("ERROR: Symbols not defined in", params['_name_'])
                return {'E': True}
        return {0: suma}

    def sigproduct(self, time, inputs, params):
        """
        Element-wise product between signals

        :purpose: Funcion que retorna la multiplicación por elementos de dos o más entradas.
        :description: Esta es una funcion tipo proceso. Toma cada valor de entrada y los va multiplicando con un valor (o vector) base.
        :param time: Valor que indica el período actual de simulación.
        :param inputs: Diccionario que entrega uno o más entradas para la función (si aplica).
        :type time: float
        :type inputs: dict
        :return: La multiplicación de todas las entradas.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: A diferencia de la función sumator, esta no comprueba que las entradas tengan las mismas dimensiones, puesto que se puede dar la ocasión donde el resultado necesitado puede ser algo de más dimensiones.
        :limitations: La función no comprueba que el resultado tenga las dimensiones deseadas, por lo que es un trabajo que debe realizar el usuario.
        :bugs: bugs

        """
        mult = 1.0
        for i in range(len(inputs)):
            mult *= inputs[i]
        return {0: mult}

    def block(self, time, inputs, params):
        """
        Generic block function for testing purposes
        """
        return {0: np.array(inputs[0])}

    def mux(self, time, inputs, params):
        """
        Multiplexer function
        """
        array = np.array(inputs[0])
        for i in range(1, len(inputs)):
            array = np.append(array, inputs[i])
        return {0: array}

    def demux(self, time, inputs, params):
        """
        Demultiplexer function
        """
        # Check input dimensions first
        if len(inputs[0]) / params['output_shape'] < params['_outputs_']:
            print("ERROR: Not enough inputs or wrong output shape in", params['_name_'])
            return {'E': True}

        elif len(inputs[0]) / params['output_shape'] > params['_outputs_']:
            print("WARNING: There are more elements in vector for the expected outputs. System will truncate. Block", params['_name_'])

        outputs = {}
        for i in range(params['_outputs_']):
            outputs[i] = inputs[0][int(params['output_shape'])*i: int(params['output_shape'])*(i+1)]
        return outputs

    def integrator(self, time, inputs, params, output_only=False, next_add_in_memory=True, dtime=0.01):
        """
        Integrator function
        """
        # Initialization (this step happens only in the first iteration)
        if params['_init_start_']:
            params['dtime'] = dtime
            params['mem'] = np.array(params['init_conds'])
            params['mem_list'] = [np.zeros(params['mem'].shape)]
            params['mem_len'] = 5.0
            params['_init_start_'] = False

            if params['method'] == 'RK45':
                params['nb_loop'] = 0
                params['RK45_Klist'] = [0, 0, 0, 0]  # K1, K2, K3, K4

            params['add_in_memory'] = True  # It defines if the saved value is sent to the next block or not

        if output_only:
            old_add_in_memory = params['add_in_memory']
            params['add_in_memory'] = next_add_in_memory  # Update for next loop
            if old_add_in_memory:
                return {0: params['mem']}
            else:
                return {0: params['aux']}
        else:
            # Checks if the new input vector dimensions match.
            if params['mem'].shape != inputs[0].shape:
                print("ERROR: Dimension Error in initial conditions in", params['_name_'])
                params['_init_start_'] = True
                return {'E': True}

            # The old value is saved
            mem_old = params['mem']

            # Integration process according to chosen method
            # Forward euler
            if params['method'] == 'FWD_RECT':
                if params['add_in_memory']:
                    params['mem'] += params['dtime'] * inputs[0]
                else:
                    params['aux'] = np.array(params['mem'] + 0.5 * params['dtime'] * inputs[0])
                    return {0: params['aux']}

            # Backwards euler
            elif params['method'] == 'BWD_RECT':
                if params['add_in_memory']:
                    params['mem'] += params['dtime'] * params['mem_list'][-1]
                else:
                    params['aux'] = np.array(params['mem'] + 0.5 * params['dtime'] * params['mem_list'][-1])
                    return {0: params['aux']}

            # Tustin
            elif params['method'] == 'TUSTIN':
                if params['add_in_memory']:
                    params['mem'] += 0.5*params['dtime'] * (inputs[0] + params['mem_list'][-1])
                else:
                    params['aux'] = np.array(params['mem'] + 0.25 * params['dtime'] * (inputs[0] + params['mem_list'][-1]))
                    return {0: params['aux']}

            # Runge-Kutta 45
            elif params['method'] == 'RK45':
                K_list = params['RK45_Klist']
                K_list[params['nb_loop']] = params['dtime'] * inputs[0]     # K1, K2, K3 or K4
                params['RK45_Klist'] = K_list
                K1, K2, K3, K4 = K_list

                if params['nb_loop'] == 0:
                    params['nb_loop'] += 1
                    params['aux'] = np.array(params['mem'] + 0.5 * K1)
                    return {0: params['aux']}
                elif params['nb_loop'] == 1:
                    params['nb_loop'] += 1
                    params['aux'] = np.array(params['mem'] + 0.5 * K2)
                    return {0: params['aux']}
                elif params['nb_loop'] == 2:
                    params['nb_loop'] += 1
                    params['aux'] = np.array(params['mem'] + K3)
                    return {0: params['aux']}
                elif params['nb_loop'] == 3:
                    params['nb_loop'] = 0
                    params['mem'] += (1 / 6) * (K1 + 2 * K2 + 2 * K3 + K4)

            aux_list = params['mem_list']
            aux_list.append(inputs[0])
            if len(aux_list) > params['mem_len']:
                aux_list = aux_list[-5:]
            params['mem_list'] = aux_list

            return {0: mem_old}

    def derivative(self, time, inputs, params):
        """
        Derivative function
        """
        if params['_init_start_']:
            params['t_old'] = time
            params['i_old'] = inputs[0]
            params['_init_start_'] = False
            return {0: 0.0}
        dt = time - params['t_old']
        di = inputs[0] - params['i_old']
        params['t_old'] = time
        params['i_old'] = inputs[0]
        return {0: np.array(di / dt)}

    def terminator(self, time, inputs, params):
        """
        Signal terminator function
        """
        return {0: np.array([0.0])}

    def export(self, time, inputs, params):
        """
        Block to save and export block signals
        """
        # To prevent saving data in the wrong iterations (integration method RK45 in use)
        if 'skip' in params.keys() and params['skip']:
            params['skip'] = False
            return {0: inputs[0]}
        # Initialization of the saving vector
        if params['_init_start_']:
            aux_vector = np.array([inputs[0]])
            try:
                params['vec_dim'] = len(inputs[0])
            except:
                params['vec_dim'] = 1

            labels = params['str_name']
            if labels == 'default':
                labels = params['_name_'] + '-0'
            labels = labels.replace(' ', '').split(',')
            if len(labels) < params['vec_dim']:
                for i in range(params['vec_dim'] - len(labels)):
                    labels.append(params['_name_'] + '-' + str(params['vec_dim'] + i - 1))
            elif len(labels) > params['vec_dim']:
                labels = labels[:params['vec_dim']]
            if len(labels) == params['vec_dim'] == 1:
                labels = labels[0]
            params['vec_labels'] = labels
            params['_init_start_'] = False
        else:
            aux_vector = params['vector']
            aux_vector = np.concatenate((aux_vector, [inputs[0]]))
        params['vector'] = aux_vector
        return {0: inputs[0]}

    def scope(self, time, inputs, params):
        """
        Function to plot block signals
        """
        # To prevent saving data in the wrong iterations (integration method RK45 in use)
        if 'skip' in params.keys() and params['skip']:
            params['skip'] = False
            return {0: inputs[0]}
        # Initialization of the saving vector
        if params['_init_start_']:
            aux_vector = np.array([inputs[0]])
            try:
                params['vec_dim'] = len(inputs[0])
            except:
                params['vec_dim'] = 1

            labels = params['labels']
            if labels == 'default':
                labels = params['_name_'] + '-0'
            labels = labels.replace(' ', '').split(',')
            if len(labels) < params['vec_dim']:
                for i in range(params['vec_dim'] - len(labels)):
                    labels.append(params['_name_'] + '-' + str(params['vec_dim'] + i - 1))
            elif len(labels) > params['vec_dim']:
                labels = labels[:params['vec_dim']]
            if len(labels) == params['vec_dim'] == 1:
                labels = labels[0]
            params['vec_labels'] = labels
            params['_init_start_'] = False
        else:
            aux_vector = params['vector']
            aux_vector = np.concatenate((aux_vector, [inputs[0]]))
        params['vector'] = aux_vector
        return {0: inputs[0]}
