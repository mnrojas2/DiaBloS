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
        :type time: float
        :type inputs: dict
        :type params['value']: float/numpy.ndarray
        :type params['delay']: float
        :type params['type']: str
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

    def gain(self, time, inputs, params):
        """
        Gain function
        """
        return {0: np.array(np.dot(params['gain'], inputs[0]))}

    def exponential(self, time, inputs, params):
        """
        Exponential function
        """
        return {0: np.array(params['a']*np.exp(params['b']*inputs[0]))}

    def sumator(self, time, inputs, params):
        """
        Sumator function
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
        """
        mult = 1.0
        for i in range(len(inputs)):
            mult *= inputs[i]
        return {0: mult}

    def block(self, time, inputs, params):
        """
        Generic block function - no actual use
        """
        return {0: np.array(inputs[0])}

    def terminator(self, time, inputs, params):
        """
        Signal terminator function
        """
        return {0: np.array([0.0])}

    def noise(self, time, inputs, params):
        """
        Normal noise function
        """
        return {0: np.array(params['sigma']**2*np.random.randn() + params['mu'])}

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
